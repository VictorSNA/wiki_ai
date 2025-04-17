#!/bin/bash

/bin/ollama serve &
pid=$!

sleep 5

echo "Retrieve model"
ollama pull mistral
echo "Done"

wait $pid