from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough

from langchain.vectorstores import Chroma
from langchain_upstage import ChatUpstage, UpstageEmbeddings


import os
import dotenv

dotenv.load_dotenv()
llm = ChatUpstage(api_key=os.getenv("UPSTAGE_API_KEY"))


# Embeddings setup
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

from template.prompt_in_eng import RAG_PROMPT_TEMPLATE

rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define the RAG chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "messages": RunnablePassthrough(),
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)