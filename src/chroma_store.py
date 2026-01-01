import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

CHROMA_DIR = "../chroma_db"
COLLECTION_NAME = "annual_reports"

def get_chroma_collection():
    print(f"Initializing ChromaDB client with persist directory: {CHROMA_DIR}")
    client = chromadb.Client(
        Settings(
            persist_directory=CHROMA_DIR,
            anonymized_telemetry=False
        )
    )

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    print(f"Collection '{COLLECTION_NAME}' created or retrieved.")
    return client, collection  # Return both client and collection

def add_chunks_to_chroma(collection, chunks):
    if not chunks:
        print("No chunks to add.")
        return
    
    documents = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):
        documents.append(chunk["text"])
        metadatas.append({
            "company": chunk["company"],
            "year": chunk["year"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"]
        })
        ids.append(f"{chunk['company']}_{chunk['year']}_{chunk['page']}_{idx}")

    print(f"Adding {len(documents)} chunks to collection...")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("Chunks added.")
    # Removed invalid persist call here