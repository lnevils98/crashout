from ollama import Client

def query(prompt: dict):
    client = Client(
        host='http://localhost:11434',
    )

    response = client.chat(
        model='llama3.2',
        messages=[
        {'role': 'user', 'content': 'How long is a marathon?'},
    ],
    )

    return response

""" def query(prompt):
    return prompt["content"] """