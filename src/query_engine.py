from chroma_store import get_chroma_collection
from llm_client import call_llm

def retrieve_chunks(query: str, n_results: int = 5):
    client, collection = get_chroma_collection()  # Unpack the tuple

    results = collection.query(  # Now collection is the correct object
        query_texts=[query],
        n_results=n_results
    )

    return results

def build_context(results):
    """
    Builds context string + citation list from Chroma results
    """
    context_blocks = []
    citations = set()

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc, meta in zip(documents, metadatas):
        context_blocks.append(
            f"[Page {meta['page']}]\n{doc}"
        )
        citations.add(meta["page"])

    context = "\n\n".join(context_blocks)
    print("Context and citations built.")
    return context, sorted(citations)


def answer_query(query: str, top_k: int = 5):
    # Step 1: Retrieve relevant chunks
    results = retrieve_chunks(query, n_results=top_k)

    # Step 2: Build context + citations
    context, citations = build_context(results)


    # Step 3: Build grounded prompt
    prompt = f"""
Context:
{context}

Question:
{query}

Instructions:
- Answer strictly using the context above
- Do not add external information
- Be concise and factual

Answer:
"""
    print("Now calling LLM with grounded prompt.")
    # Step 4: Call LLM
    answer = call_llm(context,prompt)

    return answer, citations

answer, pages = answer_query(
    "How many board meetings conducted in 2024?"
)

print("Answer:\n", answer)
print("\nCited Pages:", pages)