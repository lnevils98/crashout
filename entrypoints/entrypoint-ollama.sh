#!/bin/bash
set -e

# Start the ollama server in the background
/bin/ollama serve &
OLLAMA_PID=$!

# Wait for the server to be ready (poll the API)
#removed helath check

# Pull the model
echo "Pulling llama3.2 model..."
/bin/ollama pull llama3.2

echo "Pulling nomic-embed-text model..."
/bin/ollama pull nomic-embed-text

# Keep the server running
wait $OLLAMA_PID
