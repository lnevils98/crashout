import bs4
import curl_cffi
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from ollama import Client as OllamaClient, ChatResponse
from fastapi import HTTPException
import os
import hashlib
from app.backend.data_models import IngestRequest, IngestResponse

def parse_ul(soup: bs4.BeautifulSoup) -> str:
    """Parse an unordered list from BeautifulSoup element.
    
    Args:
        soup: BeautifulSoup element with the <ul> tag at the top level.
        
    Returns:
        Formatted string with list items prefixed with '- '.
    """
    list_items = soup.find_all('li')
    list_items = [li.text.strip() for li in list_items]
    list_items = [f'- {li}' for li in list_items]
    return "\n".join(list_items)

def parse_ol(soup: bs4.BeautifulSoup) -> str:
    """Parse an ordered list from BeautifulSoup element.
    
    Args:
        soup: BeautifulSoup element with the <ol> tag at the top level.
        
    Returns:
        Formatted string with numbered list items.
    """
    list_items = soup.find_all('li')
    list_items = [li.text.strip() for li in list_items]
    list_items = [f'{i+1}. {li}' for i, li in enumerate(list_items)]
    return "\n".join(list_items)

def chunkify(content: bs4.element.ResultSet) -> list[list[bs4.element.Tag]]:
    """Group content elements into chunks organized by headings.
    
    Each chunk starts with a heading (h1-h6) and includes all following
    elements until the next heading is encountered.
    
    Args:
        content: BeautifulSoup ResultSet of HTML elements.
        
    Returns:
        List of chunks, where each chunk is a list of BeautifulSoup Tag objects.
    """
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
    """Convert HTML element chunks into formatted text strings.
    
    Processes lists (ul/ol) with special formatting and extracts text from other elements.
    
    Args:
        chunks: List of BeautifulSoup Tag chunks to format.
        
    Returns:
        List of formatted text strings, one per chunk.
    """
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
    """Scrape and parse HTML content from a URL.
    
    Fetches a webpage, extracts relevant content (paragraphs, headings, lists),
    chunks by headings, and formats into text strings.
    
    Args:
        url: URL to scrape.
        
    Returns:
        List of formatted text chunks from the webpage.
    """
    try:
        file = curl_cffi.get(url, impersonate='chrome')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")
    
    soup = bs4.BeautifulSoup(file.text, 'html.parser')
    content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol'])

    content = chunkify(content)
    content = prettify_chunks(content)
    
    return content

def _get_ollama_client() -> OllamaClient:
    """Get or initialize the Ollama client singleton.
    
    Returns:
        OllamaClient instance configured with host from OLLAMA_HOST env var.
    """
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    _ollama_client = OllamaClient(host=host)
    return _ollama_client

def _get_qdrant_client() -> QdrantClient:
    """Get or initialize the Qdrant client singleton.
    
    Returns:
        QdrantClient instance configured with host from QDRANT_HOST env var.
    """
   
    url = os.getenv("QDRANT_HOST", "http://localhost:6333")
    _qdrant_client = QdrantClient(url=url)
    return _qdrant_client

def embed(text: str) -> list[float]:
    """Generate embeddings for text using Ollama.
    
    Args:
        text: Text to embed.
        
    Returns:
        List of float values representing the text embedding.
    """
    _ollama_client = _get_ollama_client()
    try:
        response: ChatResponse = _ollama_client.embed(model="nomic-embed-text", input=text) # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate embedding: {e}")
    return response.embeddings[0] 

def qdrant_write(document: str, collection: str) -> None:
    """Embed and store a document in Qdrant vector database.
    
    Creates a document embedding, generates a unique ID, and stores it in the
    specified collection. Creates the collection if it doesn't exist.
    
    Args:
        document: Text document to store.
        collection: Name of the Qdrant collection.
    """
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
    """Generate a unique ID for a document using SHA256 hash.
    
    Normalizes the document text and creates a deterministic hash ID.
    
    Args:
        document: Text to hash.
        truncate: Number of hash characters to return. Defaults to 32.
        
    Returns:
        Hex digest string of specified length.
    """
    normalized = " ".join(document.split()).strip().lower()
    encoded = normalized.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(encoded)
    return hash.hexdigest()[:truncate]

def extract_and_store(url: str, collection: str) -> int:
    """Scrape a URL and store all content chunks in Qdrant.
    
    Args:
        url: URL to scrape.
        collection: Qdrant collection to store content in.
        
    Returns:
        Number of content chunks that were ingested.
    """
    content = scrape(url)
    for i in content:
        qdrant_write(i, collection=collection)
    return len(content)

def ingest(ingest_request: IngestRequest) -> IngestResponse:
    """Main ingestion function to process IngestRequest and store content.
    
    Currently supports webpage ingestion. Scrapes the specified URL and stores
    all content chunks in the specified Qdrant collection.
    
    Args:
        ingest_request: IngestRequest containing type, location (URL), and collection name.
        
    Returns:
        IngestResponse confirming successful ingestion with metadata.
    """
    if ingest_request.type == "webpage":
        chunks_ingested = extract_and_store(ingest_request.location, collection=ingest_request.collection)
        return IngestResponse(
            status="success",
            message=f"Successfully ingested {chunks_ingested} content chunks from {ingest_request.location}",
            collection=ingest_request.collection,
            chunks_ingested=chunks_ingested
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported ingest type: {ingest_request.type}")