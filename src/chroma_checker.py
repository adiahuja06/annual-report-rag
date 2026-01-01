import chromadb
from chromadb.config import Settings

CHROMA_DIR = "../chroma_db"

client = chromadb.Client(Settings(
    persist_directory=CHROMA_DIR,
    anonymized_telemetry=False
))

print("Collections:", client.list_collections())