from fastapi import FastAPI
from pydantic import BaseModel

#from ingest import ingest_document
from app.query import query

app = FastAPI()

class IngestRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    role: str
    content: str

@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    #ingest_document(payload.doc_id, payload.text, {})
    #return {"status": "ok"}
    pass

@app.post("/query")
def query_endpoint(prompt: QueryRequest):
    answer = query(prompt)
    return {"message": answer}
