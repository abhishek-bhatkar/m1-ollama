# Benchmark - M1 Pro 16GB / qwen3.5-9b-32k

Date: 2026-09-27. Ollama 0.34.4, `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`.

## Config

- Model: `qwen3.5-9b-32k` (FROM qwen3.5:9b, num_ctx 32768, temp 0.6, think false)
- `ollama ps`: 6.1GB, 100% GPU, CONTEXT 32768

## Results

| Test | Prompt | eval_count | Time | tok/s |
|------|--------|------------|------|-------|
| Smoke | "Reply with exactly: LOCAL OK" | - | 8.0s total (cold load) | - |
| Story | "Write a 30-word story about a robot." think=false stream=false | 40 | 4.0s eval | 10.0 |

Response: "The robot built a garden, watering flowers with its mechanical arm..."

## Interpretation

- 10 tok/s at 32K ctx on M1 is correct. Reddit expects 12-22 tok/s at 4K ctx for 8B class; larger ctx + q8_0 KV cache costs throughput.
- For speed: drop to num_ctx 8192-16384 or use `qwen3.5:4b` (~50 tok/s class).
- For quality: keep 32K, think off. Enable think per-request only for hard reasoning.
- Re-run: `./scripts/benchmark.sh`
