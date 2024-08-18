from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union

from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langserve import add_routes
from langchain_core.runnables import Runnable

from chat import chain as chat_chain
from rag import rag_chain

import logging

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/main/playground")

class InputChat(BaseModel):
    """Input for the chat endpoint."""
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current situation.",
    )

# Add RAG system interface
add_routes(
    app,
    retriever_chain.with_types(input_type=InputChat),
    path="/chat_retriever",
    enable_feedback_endpoint=True,
    #enable_public_trace_link_endpoint=True,
    playground_type="chat",
)


add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    #enable_public_trace_link_endpoint=True,
    playground_type="chat",
)


add_routes(
    app,
    rag_chain.with_types(input_type=InputChat),
    path="/main",
    enable_feedback_endpoint=True,
    #enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

# Predibase integration
add_routes(
    app,
    summarize_chain.with_types(input_type=InputChat),
    path="/summarize",
    enable_feedback_endpoint=True,
    #enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

# Run the development server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)