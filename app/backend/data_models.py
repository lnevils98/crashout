from pydantic import BaseModel

class IngestRequest(BaseModel):
    type: str
    collection: str
    location: str

class QueryRequest(BaseModel):
    role: str
    content: str
    company: str

class QueryResponse(BaseModel):
    content: str