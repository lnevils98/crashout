from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from ollama import Client as OllamaClient, ChatResponse
import requests
from typing import Mapping, Any, Optional, Sequence
import os

_client: Optional["OllamaClient"] = None

def _get_client() -> OllamaClient:
    global _client
    if _client is None:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        _client = OllamaClient(host=host)
    return _client

ollama_client = _get_client()

response: ChatResponse = ollama_client.chat(model="llama3.2", messages=[{"role" : "user", "content" : "Tell me about France"}], stream=False)

print(response)