from smolagents import Tool
import pdfplumber
import camelot
import tempfile
import os
from typing import Optional
import requests


class PDFDatasheetReaderTool(Tool):
    name = "pdf_datasheet_reader"
    description = """
    Reads and extracts information from PDF datasheets. This tool can:
    - Extract all text content from PDF pages
    - Detect and extract tables with specifications
    - Handle both local file paths and URLs
    - Provide structured output with text and table data

    Input: PDF file path (local path or URL)
    Output: Structured text containing the PDF content with clearly labeled sections and tables
    """
    inputs = {
        "pdf_path": {
            "type": "string",
            "description": "Path to the PDF file (local file path or URL starting with http/https)",
        },
        "extract_tables": {
            "type": "boolean",
            "description": "Whether to extract tables using Camelot (default: True)",
            "nullable": True,
        },
    }
    output_type = "string"

    def __init__(self):
        super().__init__()

    def _download_pdf(self, url: str) -> str:
        """Download PDF from URL to temporary file"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

    def _extract_tables_from_pdf(self, pdf_path: str) -> dict:
        """Extract tables using Camelot"""
        try:
            tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

            # If lattice doesn't find tables, try stream flavor
            if len(tables) == 0:
                tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")

            extracted_tables = {}
            for i, table in enumerate(tables):
                page_num = table.page
                if page_num not in extracted_tables:
                    extracted_tables[page_num] = []

                # Convert table to readable format
                df = table.df
                table_text = f"\n[Table {i+1} on page {page_num}]\n"
                table_text += df.to_string(index=False, header=True)
                extracted_tables[page_num].append(table_text)

            return extracted_tables
        except Exception as e:
            return {"error": f"Table extraction failed: {str(e)}"}

    def _extract_text_from_pdf(self, pdf_path: str) -> dict:
        """Extract text using pdfplumber"""
        page_contents = {}

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    page_contents[i] = text.strip()

        return page_contents

    def forward(self, pdf_path: str, extract_tables: Optional[bool] = True) -> str:
        """
        Main method to read and extract information from PDF datasheets

        Args:
            pdf_path: Path to PDF file or URL
            extract_tables: Whether to extract tables (default: True)

        Returns:
            Structured string with extracted content
        """
        temp_file = None

        try:
            # Handle URL downloads
            if pdf_path.startswith(("http://", "https://")):
                temp_file = self._download_pdf(pdf_path)
                working_path = temp_file
            else:
                working_path = pdf_path

            if not os.path.exists(working_path):
                return f"Error: PDF file not found at {pdf_path}"

            # Extract text content
            text_content = self._extract_text_from_pdf(working_path)

            # Extract tables if requested
            table_content = {}
            if extract_tables:
                table_content = self._extract_tables_from_pdf(working_path)

            # Build structured output
            output = f"=== PDF DATASHEET CONTENT ===\n"
            output += f"Source: {pdf_path}\n"
            output += f"Total Pages: {len(text_content)}\n\n"

            # Combine text and tables page by page
            all_pages = sorted(
                set(list(text_content.keys()) + list(table_content.keys()))
            )

            for page_num in all_pages:
                output += f"\n{'='*60}\n"
                output += f"PAGE {page_num}\n"
                output += f"{'='*60}\n\n"

                # Add text content
                if page_num in text_content:
                    output += "--- Text Content ---\n"
                    output += text_content[page_num] + "\n\n"

                # Add tables
                if (
                    page_num in table_content
                    and not isinstance(table_content, dict)
                    or "error" not in table_content
                ):
                    if page_num in table_content:
                        output += "--- Tables ---\n"
                        for table in table_content[page_num]:
                            output += table + "\n\n"

            # Add table extraction errors if any
            if isinstance(table_content, dict) and "error" in table_content:
                output += f"\nNote: {table_content['error']}\n"

            return output

        except Exception as e:
            return f"Error reading PDF: {str(e)}"

        finally:
            # Cleanup temporary file if created
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
