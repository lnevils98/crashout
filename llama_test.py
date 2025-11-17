from ollama import Client

client = Client(
    host='http://localhost:11434',
)

response = client.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': 'Explain pods vs deployments.'},
    ],
)

print(response['message']['content'])
