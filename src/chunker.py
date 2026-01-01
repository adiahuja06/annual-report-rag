from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

def chunk_pages(pages):
    chunks = []
    for page in pages:
        texts = splitter.split_text(page["text"])
        for i, chunk in enumerate(texts):
            chunks.append({
                "company": page["company"],
                "year": page["year"],
                "page": page["page"],
                "chunk_id": i,
                "text": chunk
            })
    return chunks
