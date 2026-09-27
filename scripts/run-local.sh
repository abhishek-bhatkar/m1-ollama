#!/bin/zsh
# run-local: chat with think off (avoids M1 agent hang)
# usage: ./scripts/run-local.sh "your prompt" [model]
set -e
MODEL="${2:-qwen3.5-9b-32k}"
ollama run "$MODEL" --think=false "$1"
