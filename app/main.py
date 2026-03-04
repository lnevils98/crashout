from fastapi import FastAPI
from pydantic import BaseModel
from typing import Mapping, Any, Sequence
from fastapi.middleware.cors import CORSMiddleware

#from ingest import ingest_document
from app.backend.query_2 import query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    role: str
    content: str
    company: str

class QueryResponse(BaseModel):
    content: str

@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    #ingest_document(payload.doc_id, payload.text, {})
    #return {"status": "ok"}
    pass

@app.post("/query", response_model=QueryResponse)
def query_endpoint(prompt: QueryRequest):
    content = query(prompt)
    return QueryResponse(content=content)

#query(QueryRequest(role="user", content="What is the capital of France?", company="Trek"))
