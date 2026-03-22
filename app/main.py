from fastapi import FastAPI
from app.backend.data_models import IngestRequest, QueryRequest, QueryResponse #figure out absolute paths for testing
from fastapi.middleware.cors import CORSMiddleware
from app.backend.query import query
from app.backend.ingest import ingest

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
    ingest(payload)
    return

@app.post("/query", response_model=QueryResponse)
def query_endpoint(prompt: QueryRequest):
    return query(prompt)
    

query(QueryRequest(role="user", content="What is the capital of France?", company="Trek"))
