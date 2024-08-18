from dotenv import load_dotenv
import os
import json
import sys
import time
from tqdm import tqdm
# from langchain_community.vectorstores import Chroma
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings

# Load environment variables
load_dotenv()

# Load API keys from environment variables
UPSTAGE_API_KEY = os.getenv('UPSTAGE_API_KEY')

from ocr import load_documents_from_json

def main(input_path):
    start_time = time.time()

    # Use the recursive character splitter
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=60,
        separators=["\n\n", "\n", "\.", " ", ""]
    )

    # Load documents
    pages = load_documents_from_json(input_path)

    # Perform the splits using the splitter
    data_splits = list(tqdm(recur_splitter.split_documents(pages), desc="Splitting documents", unit="chunk"))
    print(f"Number of splits: {len(data_splits)}")

    # Vector Store 구축
    embeddings = UpstageEmbeddings(
        api_key=UPSTAGE_API_KEY,
        model="solar-embedding-1-large"
    )

    persist_directory = '../.cache/db'

    vectordb = Chroma.from_documents(
        documents=data_splits, # 위에서 처리한 데이터 
        embedding=embeddings, # upstage solar embedding 1 large
        persist_directory=persist_directory)

    vectordb.persist()
    vectordb = None

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Chunking and vector store creation for {input_path} completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chunking.py <path to OCR JSON file>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    main(input_path)