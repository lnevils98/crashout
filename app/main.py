from fastapi import FastAPI
from pydantic import BaseModel

#from ingest import ingest_document
from query import query

app = FastAPI()

class IngestRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    question: str

@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    #ingest_document(payload.doc_id, payload.text, {})
    #return {"status": "ok"}
    pass

@app.post("/query")
def query_endpoint(payload: QueryRequest):
    answer = query(payload.question)
    return {"answer": answer}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello {name}!"}
