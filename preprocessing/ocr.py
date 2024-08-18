from dotenv import load_dotenv
import os
import json
import sys
import time
from tqdm import tqdm
from langchain_upstage import UpstageLayoutAnalysisLoader
from langchain_core.documents.base import Document

# Load environment variables
load_dotenv()

# Load API keys from environment variables
UPSTAGE_API_KEY = os.getenv('UPSTAGE_API_KEY')

def main(file_path, output_path):
    start_time = time.time()
    
    # For image files, set use_ocr to True to perform OCR inference on the document before layout detection.
    loader = UpstageLayoutAnalysisLoader(file_path, split="page", api_key=UPSTAGE_API_KEY, use_ocr=True)
    
    # For improved memory efficiency, consider using the lazy_load method to load documents page by page.
    pages = list(tqdm(loader.load(), desc="Processing pages", unit="page"))
    
    # OCR 결과물을 json으로 저장
    pages_list = [
        {"text": page.page_content, "metadata": page.metadata} for page in pages
    ]

    with open(output_path, "w", encoding="utf-8") as file: 
        json.dump(pages_list, file, ensure_ascii=False, indent=4)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"OCR processing for {file_path} completed in {elapsed_time:.2f} seconds.")

def load_documents_from_json(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        docs_list = json.load(file)
    return [
        Document(page_content=doc["text"], metadata=doc["metadata"]) for doc in docs_list
    ]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ocr.py <path to PDF file> <path to save OCR JSON output>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = sys.argv[2]
    main(file_path, output_path)