from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse
from ollama import Client as OllamaClient, ChatResponse
from typing import Mapping, Any, Optional, Sequence
import os
from pydantic import BaseModel

_ollama_client: Optional["OllamaClient"] = None
_qdrant_client: Optional["QdrantClient"] = None

class QueryRequest(BaseModel): #try to consolidate classes in one file in the backend directorty
    role: str
    content: str
    company: str

system_prompt ="""You are an AI assistant that helps people with bicycle maintenance questions. You have access to the following pieces of information about bicycle maintenance, which may be relevant to the user's question. Use this information to answer the question as best you can. If the information is not relevant, you can ignore it. Always use the provided information to answer the question, and do not make up information that is not provided.
Use the provided context to answer the question."""

def _get_ollama_client() -> OllamaClient:
    global _ollama_client
    if _ollama_client is None:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        _ollama_client = OllamaClient(host=host)
    return _ollama_client

def _get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        url = os.getenv("QDRANT_HOST", "http://localhost:6333")
        _qdrant_client = QdrantClient(url=url)
    return _qdrant_client

def embed(text:str) -> list[float]:
    _ollama_client = _get_ollama_client()
    response: ChatResponse = _ollama_client.embed(model="nomic-embed-text", input=text) # type: ignore
    return response.embeddings[0] # type: ignore

def search(vector: Sequence[float], collection_name: str, limit: int) -> Sequence[str]:
    qdrant_client = _get_qdrant_client()
    results: QueryResponse = qdrant_client.query_points(
        collection_name=collection_name,
        query=vector,
        limit=limit,
    )

    return [results.points[i].payload["text"] for i in range(len(results.points))]

def build_prompt(user_input: str, context: Sequence[str], system_prompt: str) -> Sequence[Mapping[str, Any]]:
    context_block = "\n".join(
        f"[{idx+1}] {ctx}"
        for idx, ctx in enumerate(context)
    )

    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"CONTEXT:\n{context_block}"},
        {"role": "user", "content": f"QUESTION:\n{user_input}"},
    ]
    return prompt

def chat(messages: Sequence[Mapping[str, Any]], model: str = "llama3.2") -> ChatResponse:
    """
    messages: sequence of dicts or Message objects, e.g. {"role": "user", "content": "Hello"}
    Returns a ChatResponse (stream=False).
    """
    # Basic structural validation
    for m in messages:
        if isinstance(m, dict):
            if "role" not in m or "content" not in m:
                raise ValueError("message dict must contain 'role' and 'content' keys")

    ollama_client = _get_ollama_client()
    response: ChatResponse = ollama_client.chat(model=model, messages=messages, stream=False) # type: ignore

    return response

def query(query_request: QueryRequest):
    vector = embed(query_request.content)
    context = search(vector, collection_name=query_request.company, limit=3)
    prompt = build_prompt(user_input=query_request.content, context=context, system_prompt=system_prompt)
    response = chat(prompt)
    return response.message.content