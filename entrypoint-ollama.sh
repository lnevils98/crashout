#!/bin/bash
set -e

# Start the ollama server in the background
/bin/ollama serve &
OLLAMA_PID=$!

# Wait for the server to be ready (poll the API)
echo "Waiting for Ollama server to be ready..."
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Ollama server is ready!"
    break
  fi
  echo "Attempt $i/30 - waiting for server..."
  sleep 2
done

# Pull the model
echo "Pulling llama3.2 model..."
/bin/ollama pull llama3.2

# Keep the server running
wait $OLLAMA_PID
