import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()  # loads .env from project root

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in environment variables")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_API_TOKEN
)

def call_llm(prompt: str) -> str:
    response = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research assistant analyzing company annual reports. "
                    "Answer ONLY using the provided context. "
                    "If the answer is not present in the context, say "
                    "'Not found in the provided documents.'"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
