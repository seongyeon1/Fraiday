from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일의 내용을 읽어들임

PREDIBASE_API_KEY = os.getenv('PREDIBASE_API_KEY')
UPSTAGE_API_KEY = os.getenv('UPSTAGE_API_KEY')
WNB_KEY = os.getenv('WANDB_API_KEY')

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.llms import OpenAI
# from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, DirectoryLoader, PyMuPDFLoader


### Langchain으로 Layout Analysis

from langchain_upstage import UpstageLayoutAnalysisLoader
 
#file_path = "../data/snu_health4u.pdf" # 링크는 안됨
file_path = "../data/생활응급처치_길라잡이.pdf"

# For image files, set use_ocr to True to perform OCR inference on the document before layout detection.
loader = UpstageLayoutAnalysisLoader(file_path, split="page", api_key=UPSTAGE_API_KEY, use_ocr=True)
 
# For improved memory efficiency, consider using the lazy_load method to load documents page by page.
pages = loader.load()  # or loader.lazy_load()
 
# for page in pages:
#     print(page) # print the document content

# OCR 결과물을 json으로 저장
import json

pages_list = [
    {"text": page.page_content, "metadata": page.metadata} for page in pages
]

# with open("snu_health4u_ocr.json", "w", encoding="utf-8") as file: 
#     json.dump(pages_list, file, ensure_ascii=False, indent=4)

with open("../data/생활응급처치_길라잡이_ocr.json", "w", encoding="utf-8") as file: 
    json.dump(pages_list, file, ensure_ascii=False, indent=4)



# JSON 파일에서 Document 리스트 불러오기
def load_documents_from_json(file_name):

    from langchain_core.documents.base import Document

    with open(file_name, "r", encoding="utf-8") as file:
        docs_list = json.load(file)
    return [
        Document(page_content=doc["text"], metadata=doc["metadata"]) for doc in docs_list
    ]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)