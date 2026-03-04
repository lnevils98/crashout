from pydantic import BaseModel

class IngestRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    role: str
    content: str
    company: str

class QueryResponse(BaseModel):
    content: str