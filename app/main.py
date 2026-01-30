from fastapi import FastAPI
from pydantic import BaseModel
from typing import Mapping, Any, Sequence

#from ingest import ingest_document
from app.backend.query import query

app = FastAPI()

class IngestRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    role: str
    content: str

def _clean_query(raw_request: QueryRequest) -> Sequence[Mapping[str, Any]]:
    request: Mapping[str, Any] = raw_request.model_dump()
    return [request]

@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    #ingest_document(payload.doc_id, payload.text, {})
    #return {"status": "ok"}
    pass

@app.post("/query")
def query_endpoint(prompt: QueryRequest):
    cleaned_prompt = _clean_query(prompt)
    answer = query(cleaned_prompt)
    return {"message": answer}
