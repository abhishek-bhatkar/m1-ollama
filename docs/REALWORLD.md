# Real-world scenario - qwen3.5-9b-32k in T3 Code (2026-09-27)

Hardware: MacBook Pro M1, 16GB unified (~10-11GB usable). Ollama 0.34.4,
`FLASH_ATTENTION=1`, `KV_CACHE q8_0`. Model 6.6GB GGUF Q4_K_M, 100% GPU, ctx 32768.

## What was tried

1. Direct Ollama chat (API + `ollama run --think=false`): PASS.
   "Reply with exactly: LOCAL OK" -> `LOCAL OK` in ~8s cold (model load included).
2. Direct story gen (40 tokens): PASS, 10.0 tok/s.
3. `opencode run --model ollama-local/qwen3.5-9b-32k "Reply with exactly: T3 OK"`
   in `m1-ollama/`: FAIL (timeout). No output after 180s. Ollama log showed
   one slot processed 2077 tokens then went idle. Process had to be killed.

## Interpretation

- Provider wiring is correct (`opencode models ollama-local` lists the model,
  `/v1/models` serves it). Failure is not config - it is the agent loop:
  system prompt + tools + history inflate context, 9B on M1 burns ~2K tokens
  without converging, matching Reddit reports (thinking loops, Qwen3.5 tool-parser
  issues on Ollama, 16GB agent slowness vs 7x faster GPT-4o).
- Same pattern as r/LocalLLaMA "Qwen 3.5 9b stuck as agent on M1 Mini 16GB":
  fix is think-off + small scope, but full planning mode still stalls.

## Verdict (stands until re-benchmarked)

| Use in T3 Code | Result |
|----------------|--------|
| Chat / explain / summarize | Usable (~10 tok/s) |
| Single small scoped edit | Usable, slow |
| Agent / planning / multi-file refactor | Not usable - use cloud |

## How to re-test any model

Run `./scripts/bench-suite.sh <model>` (e.g. `./scripts/bench-suite.sh qwen3.5-9b-32k`).
It runs L0 (direct chat), L1 (single-file edit via API), L2 (bounded `opencode run`
with 120s timeout so hangs become FAIL instead of hanging you), and writes
`results/<model>-<timestamp>.md`. Compare new models against the baseline in
`results/` - a model only graduates to "agent usable" if L2 passes twice in a row.
