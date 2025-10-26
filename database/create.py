import chromadb
from chromadb.config import Settings
import pandas as pd
from sentence_transformers import SentenceTransformer

HOST = "localhost"
PORT = 8000
MODEL = "all-mpnet-base-v2"


def populate_chroma_from_csv(
    csv_path="database/ncm.csv", collection_name="technical_specs"
):
    """
    Populate Chroma database with data from CSV file.

    Args:
        csv_path: Path to the CSV file
        collection_name: Name of the Chroma collection to create
    """

    # Connect to Chroma server
    print(f"Connecting to Chroma server at {HOST}:{PORT}.")
    try:
        client = chromadb.HttpClient(host=HOST, port=PORT)
        print("Connected to Chroma server successfully!")
    except Exception as e:
        raise Exception(f"Failed to connect to Chroma server: {e}")

    # Load embedding model
    model = SentenceTransformer(MODEL)

    # Read CSV file
    print(f"Reading CSV file: {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", sep=",")
        print(f"Loaded {len(df)} rows from CSV")
        print(f"Columns found: {list(df.columns)}")
    except Exception as e:
        raise Exception(f"Failed to read CSV: {e}")

    # Prepare column names (handle different possible column names)
    # Assuming columns are in order: [ignored, code, description_pt, description_en]
    if len(df.columns) < 3:
        raise Exception(f"CSV must have at least 4 columns. Found: {len(df.columns)}")

    # col_ignored = df.columns[0]
    col_code = df.columns[0]
    col_desc_pt = df.columns[1]
    col_desc_en = df.columns[2]

    print(f"   Using columns:")
    print(f"   - Code: {col_code}")
    print(f"   - Portuguese: {col_desc_pt}")
    print(f"   - English: {col_desc_en}")

    # Clean data
    df = df.dropna(
        subset=[col_code, col_desc_en]
    )  # Remove rows with missing essential data
    df[col_desc_pt] = df[col_desc_pt].fillna("")  # Fill missing Portuguese descriptions
    df[col_desc_en] = df[col_desc_en].fillna("")  # Fill missing English descriptions
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
        print(f"Collection created: {collection_name}")
    except Exception as e:
        raise Exception(f"Failed to create collection: {e}")

    # Generate embeddings and add to Chroma
    print("Generating embeddings and populating database.")

    batch_size = 100  # Process in batches
    total_batches = (len(df) + batch_size - 1) // batch_size

    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i : i + batch_size]
        batch_num = (i // batch_size) + 1

        print(
            f"   Processing batch {batch_num}/{total_batches} ({len(batch_df)} items)."
        )

        # Prepare data for this batch
        documents = batch_df[col_desc_en].tolist()  # English descriptions for embedding
        ids = [f"item_{idx}" for idx in range(i, i + len(batch_df))]
        metadatas = [
            {
                "code": str(row[col_code]),
                "description_pt": str(row[col_desc_pt]),
                "description_en": str(row[col_desc_en]),
            }
            for _, row in batch_df.iterrows()
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
    CSV_FILE = "database/ncm.csv"

    populate_chroma_from_csv(CSV_FILE)
