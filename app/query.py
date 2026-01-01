import os
from typing import Mapping, Any, Optional, Sequence

# adjust import to match your ollama client package
from ollama import Client, ChatResponse

_client: Optional["Client"] = None

def _get_client() -> Client:
    global _client
    if _client is None:
        host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        _client = Client(host=host)
    return _client

def query(messages: Sequence[Mapping[str, Any]], model: str = "llama3.2") -> ChatResponse:
    """
    messages: sequence of dicts or Message objects, e.g. {"role": "user", "content": "Hello"}
    Returns a ChatResponse (stream=False).
    """
    # Basic structural validation
    for m in messages:
        if isinstance(m, dict):
            if "role" not in m or "content" not in m:
                raise ValueError("message dict must contain 'role' and 'content' keys")

    client = _get_client()
    response: ChatResponse = client.chat(model="llama3.2", messages=messages, stream=False) # type: ignore

    return response