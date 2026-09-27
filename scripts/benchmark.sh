#!/bin/zsh
# benchmark: 40-token story on qwen3.5-9b-32k, reports tok/s
set -e
MODEL="${1:-qwen3.5-9b-32k}"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"Write a 30-word story about a robot.\",\"think\":false,\"stream\":false}" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('response:', d.get('response','')[:200])
ec=d.get('eval_count',0); ed=d.get('eval_duration',1)
print(f\"eval_count: {ec} tok/s: {ec/(ed/1e9):.1f}\")
"
ollama ps
