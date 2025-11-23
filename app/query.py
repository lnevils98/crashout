from ollama import Client

def query(prompt: dict):
    client = Client(
        host='http://localhost:11434',
    )

    response = client.chat(
        model='llama3.2',
        messages=[
        prompt,
    ],
    )

    return response