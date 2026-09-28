# m1-ollama

Local LLMs on a MacBook Pro M1 / 16GB — tested, benchmarked, and wired into
[T3 Code](https://github.com/pingdotgg/t3code) (OpenCode-compatible).
No cloud needed for everyday agent work.

Hardware: Apple M1 · 16GB unified (~10–11GB usable) · Ollama 0.34.4 (brew service)

## Fleet status

| Model (Ollama) | T3 Code name | Size | Chat | Agent (L2 2x) | Role |
|---|---|---|---|---|---|
| `qwen35-4b-32k` | Qwen3.5 4B 32K (local tools) ✅ | 3.9GB | 18 tok/s | **PASS ~69s x2** | Terminal / agent work |
| `qwen25-coder-32k` | Qwen2.5-Coder 7B 32K (local agent) ✅ | 5.5GB | 7 tok/s | **PASS 110s/3s** | Codegen quality |
| `qwen3.5-9b-32k` | Qwen3.5 9B 32K (local, think off) | 6.1GB | 10 tok/s | FAIL (timeout x2) | Chat / summarize |

Full evidence: [`docs/REALWORLD.md`](docs/REALWORLD.md) · raw runs: [`results/`](results/)

**TL;DR:** the tiny 4B is the best terminal agent (top tool-calling eval, Mar 2026:
97.5%); the 7B coder writes better code; the 9B is smartest for chat but can't
close the agent loop on 16GB. Hard stuff still goes to cloud.

## Quickstart

```bash
brew install ollama && brew services start ollama
ollama pull qwen3.5:4b
printf 'FROM qwen3.5:4b\nPARAMETER num_ctx 32768\nPARAMETER temperature 0.6\n' > Modelfile
ollama create qwen35-4b-32k -f Modelfile
./scripts/status.sh       # service + models + GPU check
./scripts/bench-suite.sh qwen35-4b-32k ollama-local/qwen35-4b-32k
```

T3 Code wiring: add an `ollama-local` provider (`@ai-sdk/openai-compatible`,
`http://localhost:11434/v1`) to `~/.config/opencode/opencode.json`, or copy this
repo's [`opencode.json`](opencode.json) (pins the 4B as project default).

## Method

`scripts/bench-suite.sh` grades every model the same way: **L0** direct chat,
**L1** single-file fix via API, **L2** bounded `opencode run` (120s timeout, hangs
become FAIL). A model graduates to "agent usable" only on **L2 PASS twice in a row**.
Reddit + benchmark research behind the picks: [`docs/NOTES.md`](docs/NOTES.md).

## Layout

```
m1-ollama/
  opencode.json        # project default: local 4B (copy to any project)
  docs/NOTES.md        # Reddit + Sep-2026 research (MLX vs GGUF, 16GB tiers)
  docs/BENCHMARK.md    # tok/s measurements on this M1
  docs/REALWORLD.md    # T3 Code thread outcomes + current recommendation
  results/             # every bench-suite run, one file per model run
  scripts/bench-suite.sh|py  # the grader (timeouts included)
  scripts/status.sh|benchmark.sh|run-local.sh|fixtures/
```

## Lessons (M1 16GB)

- GGUF, not MLX (no native bf16 on M1; MLX build is also 2GB heavier).
- Thinking mode OFF for agents (hangs the loop); 20–32K ctx, not 128K.
- First agent call of the day is slow (~1–2 min cold prefill); then seconds.
- T3 Code's agent prompt is ~13K tokens — disable unused MCP servers.
- Small models need explicit per-step tool instructions, not open-ended asks.
