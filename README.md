# m1-ollama

Local LLM setup for MacBook Pro M1 / 16GB unified memory.
Reddit-verified daily driver: `qwen3.5:9b` GGUF Q4_K_M, thinking off, 32K context.

## Hardware

- Chip: Apple M1 (8-core), arm64
- RAM: 16GB unified ( ~10-11GB usable after macOS )
- Disk free at setup: 99GB

## Stack

- Runtime: Ollama 0.34.4 (brew service, autostart)
- Env: `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_CONTEXT_LENGTH=32000`
- Model: `qwen3.5:9b` (6.6GB) + wrapper `qwen3.5-9b-32k` (num_ctx 32768, think off)
- Provider: `ollama-local` in `~/.config/opencode/opencode.json` -> `http://localhost:11434/v1`

## Quick start

```bash
./scripts/status.sh      # service + model + GPU check
./scripts/benchmark.sh   # 40-token story, reports tok/s
./scripts/bench-suite.sh qwen3.5-9b-32k ollama-local/qwen3.5-9b-32k
# full real-world suite (L0 chat, L1 edit, L2 bounded agent) -> results/
ollama run qwen3.5-9b-32k "Reply with exactly: LOCAL OK"
```

## Real-world verdict in T3 Code

See `docs/REALWORLD.md` + `results/` baseline. Chat/edit = usable (~10 tok/s),
agent/planning loops = not usable (L2 timeout). A model graduates to
"agent usable" only if L2 passes twice in a row via `bench-suite.sh`.

## Why this model

See `docs/NOTES.md` (Reddit consensus Sep 2026) and `docs/BENCHMARK.md` (measured 10.0 tok/s, 100% GPU, 32K).

## Why GGUF not MLX

M1 lacks native bf16, Qwen3.5 hybrid attention is better in llama.cpp, MLX build is 8.9GB vs 6.6GB GGUF. Details in `docs/NOTES.md`.
