from chromadb import ClientAPI, HttpClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


MODEL = "all-mpnet-base-v2"
ENCODING = "utf-8"
SEPARATOR = ","


def connect_chroma() -> ClientAPI:
    """Connect to Chroma database."""
    HOST = os.getenv("CHROMA_HOST")
    PORT = os.getenv("CHROMA_PORT")
    try:
        client = HttpClient(host=HOST, port=PORT)
        return client
    except Exception as e:
        raise Exception(f"Failed to connect to Chroma server: {e}")


def read_csv(ncm_path: str, tipi_path: str) -> pd.DataFrame:
    """
    Merge the NCM and TIPI CSV files.

    Args:
        ncm_path: Path to the NCM CSV file
        tipi_path: Path to the TIPI CSV file
    """
    try:
        data_ncm = pd.read_csv(ncm_path, encoding="utf-8", sep=",")
        data_tipi = pd.read_csv(tipi_path, encoding="utf-8", sep=",")

        df = pd.merge(
            data_ncm[["CO_NCM", "NO_NCM_POR", "NO_NCM_ING"]],
            data_tipi[["NCM", "EX"]],
            left_on="CO_NCM",
            right_on="NCM",
            how="inner",
        )

        df = df.drop(columns=["CO_NCM"])

        print(df.columns)

        assert len(df.columns) == 4

        return df
    except Exception as e:
        raise Exception(f"Failed to read CSV: {e}")


def populate_chroma_from_csv(
    ncm_path: str,
    tipi_path: str,
    collection_name="technical_specs",
):
    """
    Populate Chroma database with data from CSV file.

    The CSV file must follow this rules:
    - Encoding: UTF-8
    - Separator symbol: comma (',')
    - Columns must follow this order:
        - NCM code
        - EX code
        - Portuguese description
        - English description

    Args:
        ncm_path: Path to the NCM CSV file
        tipi_path: Path to the TIPI CSV file
        collection_name: Name of the Chroma collection to create
    """
    # Connect to Chroma server
    client = connect_chroma()

    # Load embedding model
    model = SentenceTransformer(MODEL)

    # Read CSV file
    print(f"Reading CSV files")
    df = read_csv(ncm_path=ncm_path, tipi_path=tipi_path)
    print(f"Loaded {len(df)} rows from CSV")
    print(f"Columns found: {list(df.columns)}")

    # Clean data
    # Remove rows with missing essential data
    df = df.dropna(subset=["NCM", "NO_NCM_ING", "NO_NCM_POR"])
    print(f"{len(df)} valid rows after cleaning")

    # Create or get collection
    try:
        # Delete existing collection if it exists
        try:
            client.delete_collection(name=collection_name)
        except:
            pass

        collection = client.create_collection(
            name=collection_name,
            metadata={
                "description": "Technical specifications with PT/EN descriptions"
            },
        )
        print(f"\nCollection created: {collection_name}")
    except Exception as e:
        raise Exception(f"Failed to create collection: {e}")

    # Generate embeddings and add to Chroma
    print("Generating embeddings and populating database.")
    documents = df["NO_NCM_ING"].tolist()  # English descriptions for embedding
    ids = [f"item_{idx}" for idx in range(len(df))]
    metadatas = [
        {
            "ncm": str(row["NCM"]),
            "ex": str(row["EX"]),
            "description_pt": str(row["NO_NCM_POR"]),
            "description_en": str(row["NO_NCM_ING"]),
        }
        for _, row in df.iterrows()
    ]

    # Generate embeddings
    embeddings = model.encode(documents, device="cpu").tolist()

    # Add to collection
    collection.add(
        embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids
    )

    print(f"Successfully populated {len(df)} items into Chroma!")
    print(f"Collection stats: {collection.count()} items")


if __name__ == "__main__":
    populate_chroma_from_csv(
        ncm_path="./database/data/ncm.csv", tipi_path="./database/data/tipi.csv"
    )
