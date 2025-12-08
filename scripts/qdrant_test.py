from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import requests

#client = QdrantClient(host="localhost", port=6333)

url = "http://localhost:11434/api/embed"

""" payload = {
    "model": "nomic-embed-text",
    "input": "Hello world"
}

response = requests.post(url, json=payload)
response.raise_for_status()

data = response.json()
print(data)
print(len(data["embeddings"][0])) """

def embed(text:str):
    payload = {
        "model": "nomic-embed-text",
        "input": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["embeddings"][0]

qdrant_client = QdrantClient(host="localhost", port=6333)

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
    limit=3
)

print("---")
print(results)
print(type(results))
    #print(r.payload["text"], "score:", r.score)
