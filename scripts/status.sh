#!/bin/zsh
# status: ollama service + models + gpu load
set -e
echo "== service =="
brew services info ollama 2>&1 | head -n 5
echo "== api =="
curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; d=json.load(sys.stdin); print('models:', [m.get('name') for m in d.get('models',[])])"
echo "== ollama =="
ollama list
ollama ps
