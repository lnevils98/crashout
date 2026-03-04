from fastapi import FastAPI
from app.backend.data_models import IngestRequest, QueryRequest, QueryResponse
from fastapi.middleware.cors import CORSMiddleware
from app.backend.query import query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    #ingest_document(payload.doc_id, payload.text, {})
    #return {"status": "ok"}
    pass

@app.post("/query", response_model=QueryResponse)
def query_endpoint(prompt: QueryRequest):
    return query(prompt)
    

query(QueryRequest(role="user", content="What is the capital of France?", company="Trek"))
