from ollama import Client

def query(message):
     client = Client(
         host='http://localhost:11434',
     )

     response = client.chat(
         model='llama3.2',
         message=message,
     )

     return response['message']['content']