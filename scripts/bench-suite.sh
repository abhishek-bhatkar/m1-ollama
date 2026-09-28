#!/bin/zsh
# bench-suite.sh: wrapper so docs stay `./scripts/bench-suite.sh <model>`
# usage: ./scripts/bench-suite.sh qwen3.5-9b-32k [opencode-model]
set -e
SCRIPT_DIR="${0:A:h}"
python3 "$SCRIPT_DIR/bench-suite.py" "$@"
