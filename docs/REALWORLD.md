# Real-world scenarios in T3 Code (M1 16GB, updated 2026-09-28)

Hardware: MacBook Pro M1, 16GB unified (~10-11GB usable). Ollama 0.34.4,
`FLASH_ATTENTION=1`, `KV_CACHE q8_0`.

## A. qwen3.5-9b-32k (6.6GB) - 2026-09-27: agent FAIL

1. Direct chat: PASS (`LOCAL OK` ~8s cold). Story 40 tokens: PASS, 10.0 tok/s.
2. `opencode run --model ollama-local/qwen3.5-9b-32k "Reply with exactly: T3 OK"`:
   FAIL (timeout). No output after 180s; slot burned 2077 tokens then idled.
   Same again via bench-suite (120s timeout): FAIL.
   Cause: agent loop + thinking/tool-parser issues on Qwen3.5 via Ollama.
   Verdict: chat/small edits only, not agent. Baseline: `results/qwen3.5-9b-32k-20260928-1216.md`.

## B. qwen25-coder-32k (4.7GB) - 2026-09-28: agent GRADUATED ✅

`FROM qwen2.5-coder:7b`, num_ctx 32768. Provider entry `ollama-local/qwen25-coder-32k`.

| Tier | Run 1 (1243, cold) | Run 2 (1245, warm) |
|------|--------------------|--------------------|
| L0a exact | PASS 3.1s | PASS 0.8s |
| L0b story | PASS 7.3 tok/s | PASS 7.4 tok/s |
| L1 edit | PASS 7.2 tok/s | PASS 7.3 tok/s |
| L2 agent | PASS 110.8s | PASS 2.9s |

L2 passed twice in a row -> **graduated to "agent usable"** per suite rule.
Note the cold/warm split: first-ever agent invocation took 110s (model load +
agent exploration), then 3s warm. In T3 Code, expect the first agent call of
the day to be slow; keep tasks small and scoped. Heavy multi-file refactors
still belong on cloud.
Baselines: `results/qwen25-coder-32k-20260928-1243.md`, `...-1245.md`.

## Current recommendation

- T3 Code agent (local): `ollama-local/qwen25-coder-32k`
- T3 Code chat/summarize: `ollama-local/qwen3.5-9b-32k` (smarter, ~10 tok/s)
- Hard tasks: cloud (Muse Spark / Claude).

## How to re-test any model

Run `./scripts/bench-suite.sh <model>` (e.g. `./scripts/bench-suite.sh qwen3.5-9b-32k`).
It runs L0 (direct chat), L1 (single-file edit via API), L2 (bounded `opencode run`
with 120s timeout so hangs become FAIL instead of hanging you), and writes
`results/<model>-<timestamp>.md`. Compare new models against the baseline in
`results/` - a model only graduates to "agent usable" if L2 passes twice in a row.
