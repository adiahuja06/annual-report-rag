import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = "../chroma_db"
COLLECTION_NAME = "annual_reports"

def get_chroma_collection():
    print(f"Initializing ChromaDB PersistentClient at: {CHROMA_DIR}")
    
    # FIX: Use PersistentClient instead of Client + Settings
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    
    print(f"Collection '{COLLECTION_NAME}' ready.")
    return client, collection

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
            "company": chunk.get("company", "Unknown"),
            "year": chunk.get("year", 0),
            "page": chunk.get("page", 0),
            "chunk_id": chunk.get("chunk_id", idx)
        })
        # Note: Ensure IDs are unique. Using idx at the end is good practice.
        ids.append(f"{chunk['company']}_{chunk['year']}_{chunk['page']}_{idx}")

    print(f"Adding {len(documents)} chunks to collection...")
    
    # It's better to add in batches if the list is extremely large
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("Chunks added and automatically persisted.")