import bs4
import curl_cffi
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from ollama import Client as OllamaClient, ChatResponse
from typing import Mapping, Any, Optional, Sequence
import os
import hashlib
from app.backend.data_models import IngestRequest

def parse_ul(soup: bs4.BeautifulSoup) -> str:
    list_items = soup.find_all('li')
    list_items = [li.text.strip() for li in list_items]
    list_items = [f'- {li}' for li in list_items]
    return "\n".join(list_items)

def parse_ol(soup: bs4.BeautifulSoup) -> str:
    list_items = soup.find_all('li')
    list_items = [li.text.strip() for li in list_items]
    list_items = [f'{i+1}. {li}' for i, li in enumerate(list_items)]
    return "\n".join(list_items)

def chunkify(content: bs4.element.ResultSet) -> list[list[bs4.element.Tag]]:
    bs4_chunks = []
    i = 0
    while i < len(content):
        element = content[i]
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            chunk = [element]
            i += 1
            while i < len(content) and content[i].name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                chunk.append(content[i])
                i += 1
            bs4_chunks.append(chunk)
        else:
            i += 1  # Skip non-heading elements or handle them separately
    return bs4_chunks  # Fix: Return the correct variable

def prettify_chunks(chunks: list[list[bs4.element.Tag]]) -> list[str]:
    str_chunks = []  # Initialize list for strings
    for chunk in chunks:
        processed = []
        for element in chunk:
            if element.name == 'ul':
                processed.append(parse_ul(element))
            elif element.name == 'ol':
                processed.append(parse_ol(element))
            else:
                processed.append(element.text.strip())
        str_chunks.append("\n\n".join(processed))
    return str_chunks

def scrape(url: str) -> list[str]:
    file = curl_cffi.get(url, impersonate='chrome')
    soup = bs4.BeautifulSoup(file.text, 'html.parser')
    content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol'])

    content = chunkify(content)
    content = prettify_chunks(content)
    
    return content

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
    return response.embeddings[0] 

def qdrant_write(document: str, collection: str) -> None:
    vector: list[float] = embed(document)
    point = PointStruct(
        id=document_id(document), #automatically translated to UUID
        vector=vector,
        payload={"text": document}
        )
    
    qdrant_client = _get_qdrant_client()

    if qdrant_client.collection_exists(collection_name=collection):
        pass
    else:
        qdrant_client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=len(vector),
                distance=Distance.COSINE
            )
        )

    qdrant_client.upsert(
        collection_name=collection,
        points=[point],
    )

def document_id(document: str, truncate: int = 32) -> str:
    normalized = " ".join(document.split()).strip().lower()
    encoded = normalized.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(encoded)
    return hash.hexdigest()[:truncate]

def extract_and_store(url: str, collection: str) -> None:
    content = scrape(url)
    for i in content:
        qdrant_write(i, collection=collection)

def ingest(ingest_request: IngestRequest) -> None:
    if ingest_request.type == "webpage":
        extract_and_store(ingest_request.location, collection=ingest_request.collection)
    else:
        pass

ingest_request = IngestRequest(
    type="webpage",
    collection="test_collection",
    location="https://www.parktool.com/en-us/blog/repair-help/rear-derailleur-adjustment"
)    

_ollama_client: Optional["OllamaClient"] = None
_qdrant_client: Optional["QdrantClient"] = None

ingest(ingest_request)