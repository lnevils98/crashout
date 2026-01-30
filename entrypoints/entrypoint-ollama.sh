#!/bin/bash
set -e

# Start the ollama server in the background
/bin/ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama server to be ready..."
until /bin/ollama list > /dev/null 2>&1; do
  sleep 2
done

# Pull the models
echo "Pulling llama3.2 model..."
/bin/ollama pull llama3.2

echo "Pulling nomic-embed-text model..."
/bin/ollama pull nomic-embed-text

# Keep the server running
wait $OLLAMA_PID

