from pathlib import Path
from text_parser import parse_text_file
from chunker import chunk_pages
from chroma_store import get_chroma_collection, add_chunks_to_chroma
# CONFIG — change for each new PDF
TXT_FILE = Path("../data/processed_text/AnnualReportFY2024-25.txt")
COMPANY = "SBI"
YEAR = 2024

def main():
    # Step 1: Parse TXT → structured pages
    pages = parse_text_file(TXT_FILE, company=COMPANY, year=YEAR)
    if not pages:
        print("No pages found in the file!")
        return

    # Step 2: Split pages → chunks
    chunks = chunk_pages(pages)
    if not chunks:
        print("No chunks created from pages!")
        return

    print(f"Total chunks created: {len(chunks)}")

    # Step 3: Add chunks to ChromaDB
    client, collection = get_chroma_collection()  # Unpack client and collection
    add_chunks_to_chroma(collection, chunks)

    print("Chunks successfully added to ChromaDB")
    # Removed persist call as it's not needed and causes errors

if __name__ == "__main__":
    main()