from ollama import Client

prompt = {'role': 'user', 'content': 'How long is a marathon?'}

client = Client(
    host='http://localhost:11434',
)

response = client.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': 'How long is a marathon?'},
    ],
)

print(response['message']['content'])