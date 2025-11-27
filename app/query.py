import os
from typing import Mapping, Any
from ollama import Client


def query(prompt: Mapping[str, Any]):
    # Use OLLAMA_HOST env var when running inside Docker Compose so the
    # FastAPI container talks to the `ollama` service on the Docker network.
    # Default to the compose service name (ollama) and port 11434.
    host = os.getenv("OLLAMA_HOST", "http://ollama:11434")

    client = Client(host=host)

    response = client.chat(
        model='llama3.2',
        messages=[prompt],
    )

    return response