import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in environment variables")

# Switch to a model that supports Chat Completion
client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct", 
    token=HF_API_TOKEN
)

def call_llm(context: str, question: str) -> str:
    # Combine context and question so the model actually has data to analyze
    full_prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
    
    try:
        response = client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a research assistant analyzing company annual reports. "
                        "Answer ONLY using the provided context. "
                        "If the answer is not present, say 'Not found in the provided documents.'"
                    )
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Example Usage:
print(call_llm("Revenue was $10M in 2023.", "What was the revenue?"))