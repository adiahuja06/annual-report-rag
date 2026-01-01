from pathlib import Path
import pdfplumber

RAW_PDF_DIR = Path("data/raw_pdfs")
OUTPUT_DIR = Path("data/processed_text")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_with_page_numbers(pdf_path: Path):
    extracted_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                extracted_pages.append({
                    "page": page_number,
                    "text": text
                })

    return extracted_pages


def process_all_pdfs():
    for pdf_file in RAW_PDF_DIR.glob("*.pdf"):
        print(f"Processing: {pdf_file.name}")

        pages = extract_text_with_page_numbers(pdf_file)
        output_file = OUTPUT_DIR / f"{pdf_file.stem}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            for page in pages:
                f.write(f"\n\n--- PAGE {page['page']} ---\n\n")
                f.write(page["text"])

        print(f"Saved: {output_file.name}")


if __name__ == "__main__":
    process_all_pdfs()
