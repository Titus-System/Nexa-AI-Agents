import chromadb
from sentence_transformers import SentenceTransformer
import sys
from smolagents import tool

HOST = "localhost"
PORT = 8000
MODEL = "all-mpnet-base-v2"
COLLECTION_NAME = "technical_specs"
N_RESULTS = 5


@tool
def query_chroma(query_text: str) -> list[dict]:
    """
    Query the Chroma database for the most semantically similar technical product specifications in Portuguese.

    This tool takes an English product description, searches the Chroma vector database,
    and returns a ranked list of the most relevant matches, including product NCM and EX codes,
    Portuguese and English descriptions, and similarity scores.

    Args:
        query_text (str): The product description in English to search for.
            Example: "Connectors for printed circuits,f/tension<=1kv"

    Returns:
        list[dict]: A list of matching product specifications, each represented as a dictionary with the following keys:
            - ncm_code (str): The product NCM classification code.
            - ex_code (str): The product EX classification code.
            - description_pt (str): The product description in Portuguese.
            - description_en (str): The product description in English.
            - similarity (float): A similarity score between 0 and 1, where 1.0 means an exact semantic match.

    Example:
        Input: query_text = "Connectors for printed circuits,f/tension<=1kv"
        Output:query_chroma(query_text)
        [
            {
                "ncm": "85369040",
                "ex": "0",
                "description_pt": "Conectores para circuito impresso, para uma tensão não superior a 1.000 V",
                "description_en": "Connectors for printed circuits,f/tension<=1kv",
                "similarity": 1.0000
            },
            {
                "ncm": "85369050",
                "ex": "1",
                "description_pt": "Terminais de conexão para capacitores, mesmo montados em suporte isolante, para uma tensão não superior a 1.000 V",
                "description_en": "Connectors for printed circuits,incl.mount.insul.backin",
                "similarity": 0.3118
            },
            {
                "ncm": "85369030",
                "ex": "0",
                "description_pt": "Soquetes para microestruturas eletrônicas, para uma tensão não superior a 1.000 V",
                "description_en": "Sockets f/electronic microstructures,f/tension<=1kv",
                "similarity": 0.2745
            },
            {
                "ncm": "85369010",
                "ex": "0",
                "description_pt": "Conectores para cabos planos constituídos por condutores paralelos isolados individualmente, para uma tensão não superior a 1.000 V",
                "description_en": "Connectors f/flat cables parallel conductors, t<=1kv",
                "similarity": 0.2125
            },
            {
                "ncm": "85444200",
                "ex": "1",
                "description_pt": "Outros condutores elétricos tensão <= 100 v, com peças de conexão",
                "description_en": "Other electric conductors f/tension<=100v, with pieces of connection",
                "similarity": 0.1357
            }
        ]

    Notes:
        - Similarity values are calculated as (1 - distance) between embeddings.
        - The results are sorted in descending order of similarity.
        - The Chroma database must be initialized and contain bilingual embeddings for accurate matching.
        - The number of results is 5.
    """

    # Connect to Chroma server
    try:
        client = chromadb.HttpClient(host=HOST, port=PORT)
    except Exception as e:
        raise Exception(f"Failed to connect to Chroma server: {e}.")

    # Load embedding model
    model = SentenceTransformer(MODEL)

    # Get collection
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        raise Exception(f"Collection '{COLLECTION_NAME}' not found: {e}")

    # Generate query embedding
    query_embedding = model.encode(query_text, device="cpu").tolist()

    # Search
    results = collection.query(query_embeddings=[query_embedding], N_RESULTS=N_RESULTS)

    if not results["ids"][0]:
        return []

    output_results = []

    for i, (id, metadata, distance) in enumerate(
        zip(results["ids"][0], results["metadatas"][0], results["distances"][0]), 1
    ):
        ncm = metadata.get("ncm", "N/A")
        ex = metadata.get("ex", "N/A")
        desc_pt = metadata.get("description_pt", "N/A")
        desc_en = metadata.get("description_en", "N/A")

        output_results.append(
            {
                "ncm": ncm,
                "ex": ex,
                "description_pt": desc_pt,
                "description_en": desc_en,
                "similarity": 1 - distance,
            }
        )

    return output_results
