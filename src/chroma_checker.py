import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = "../chroma_db"
COLLECTION_NAME = "annual_reports"

def get_chroma_collection():
    print(f"Loading ChromaDB PersistentClient from: {CHROMA_DIR}")
    
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    
    print(f"Collection '{COLLECTION_NAME}' loaded.")
    return collection

def test_collection(collection):
    # Check item count
    count = collection.count()
    print(f"Collection contains {count} items.")
    
    if count == 0:
        print("No data found in collection.")
        return
    
    # Perform a sample query
    query_text = "How many independent directors were there in 2024?"  # Example query
    results = collection.query(
        query_texts=[query_text],
        n_results=3  # Return top 3 results
    )
    
    print(f"Sample query: '{query_text}'")
    print("Top results:")
    for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0])):
        print(f"{i+1}. Page {meta['page']} (Distance: {dist:.4f}): {doc[:100]}...")  # Truncate text for readability

if __name__ == "__main__":
    collection = get_chroma_collection()
    test_collection(collection)