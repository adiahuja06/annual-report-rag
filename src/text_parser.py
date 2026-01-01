from pathlib import Path
import re

def parse_text_file(file_path: Path, company: str, year: int):
    pages = []
    current_page = None
    buffer = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            page_match = re.match(r"--- PAGE (\d+) ---", line.strip())
            if page_match:
                if current_page is not None:
                    pages.append({
                        "company": company,
                        "year": year,
                        "page": current_page,
                        "text": " ".join(buffer).strip()
                    })
                current_page = int(page_match.group(1))
                buffer = []
            else:
                buffer.append(line.strip())

    if current_page is not None:
        pages.append({
            "company": company,
            "year": year,
            "page": current_page,
            "text": " ".join(buffer).strip()
        })

    return pages
#The below is for testing purpose only
# pages = parse_text_file(
#     Path("../data/processed_text/AnnualReportFY2024-25.txt"),
#     company="SBI",
#     year=2024
# )

# print(len(pages))
# print(pages[12])
