from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from ollama import Client as OllamaClient, ChatResponse
import requests
from typing import Mapping, Any, Optional, Sequence
import os

url = "http://localhost:11434/api/embed"
_client: Optional["OllamaClient"] = None

def _get_client() -> OllamaClient:
    global _client
    if _client is None:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        _client = OllamaClient(host=host)
    return _client

def embed(text:str) -> Sequence[float]:
    _client = _get_client()
    response: ChatResponse = _client.embed(model="nomic-embed-text", input=text) # type: ignore
    return response.embeddings[0] # type: ignore

qdrant_client = QdrantClient(host="localhost", port=6333) # mirror Ollama setup

qdrant_client.recreate_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

documents = [
    "The capital of France is Paris.",
    "Machine learning enables computers to learn from data.",
    "Special Forces operations require precise intelligence."
]

points = []
for i, doc in enumerate(documents):
    vec = embed(doc)
    points.append(
        PointStruct(
            id=i,
            vector=vec,
            payload={"text": doc}
        )
    )

qdrant_client.upsert(collection_name="test_collection", points=points)

query = embed("Tell me about France")

results = qdrant_client.query_points(
    collection_name="test_collection",
    query=query,
    limit=2
)

print("---")
print(results)
print(results.points[0].payload["text"])
