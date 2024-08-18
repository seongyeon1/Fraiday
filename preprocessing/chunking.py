# Chunking.py
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
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, DirectoryLoader, PyMuPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from ocr import load_documents_from_json

# Use the recursive character splitter
recur_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=60,
    separators=["\n\n", "\n", "\.", " ", ""]
)

# # 불러오기
# pages = load_documents_from_json("../data/snu_health4u_ocr.json")
pages = load_documents_from_json("../data/생활응급처치_길라잡이_ocr.json")

# Perform the splits using the splitter
data_splits = recur_splitter.split_documents(pages)
print(data_splits)
print("Number of splits:", len(data_splits))

# Print a random chunk
import random
content = random.choice(data_splits).page_content
print("Content length:", len(content))
print(content)

# Vector Store 구축
from langchain_upstage import UpstageEmbeddings
 
embeddings = UpstageEmbeddings(
  api_key=UPSTAGE_API_KEY,
  model="solar-embedding-1-large"
)

# Test
doc_result = embeddings.embed_documents(
    ["SOLAR 10.7B: Scaling Large Language Models with Simple yet Effective Depth Up-Scaling.", "DUS is simple yet effective in scaling up high performance LLMs from small ones."]
)

query_result = embeddings.embed_query("What makes Solar LLM small yet effective?")
print(query_result)

## ChromaDB 생성
#- 대규모 벡터 데이터를 효율적으로 저장, 검색, 관리하기 적합하다.
#- 오픈소스 vector database로서, Apache 2.0 or MIT License에 해당

persist_directory = '../.cache/db'

vectordb = Chroma.from_documents(
    documents=data_splits, # 위에서 처리한 데이터 
    embedding=embeddings, # upstage solar embedding 1 large
    persist_directory=persist_directory)

vectordb.persist()
vectordb = None

from langchain_upstage import UpstageEmbeddings


embeddings = UpstageEmbeddings(
  api_key=os.getenv("UPSTAGE_API_KEY"),
  model="solar-embedding-1-large"
)

persist_directory = '../.cache/db'

vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)

retriever = vectordb.as_retriever()
# retriever = vectordb.as_retriever(search_kwargs={"k": 3}) #결과 k개 반환하고 싶을 때