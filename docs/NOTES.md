# Notes - M1 16GB local LLM (Reddit + web, Sep 2026)

## Consensus

- Daily driver range for 16GB Apple Silicon: 4B-9B Q4_K_M. 13B borderline, 27B+ thrashes.
- Top 2026 picks: `qwen3.5:9b` (best overall), `qwen3.5:4b` (fastest usable), `gemma4:12b` (multimodal), `qwen2.5-coder:7b` (chat/edits), `phi4-mini` (CPU-only).
- Old defaults (Llama 3.1 8B, Mistral 7B, Gemma 2 9B) deprecated for new builds per Sep 2026 guides.

## Qwen3.5-9B specifics

- 9.7B params, Q4_K_M 6.6GB, 256K max ctx, vision+tools, Apache 2.0.
- Scores: 82.5% MMLU-Pro, 81.7% GPQA Diamond, 65.6 LiveCodeBench v6.
- Only 8/32 layers grow KV cache -> pushes further context than peers.
- Thinking mode hangs as agent on 16GB Macs (OpenCode/Claude Code planning mode stalls). Fix: `--think=false` / `"think":false` / `/set nothink`.
- Recommended: 20-32K ctx on 16GB, temp 0.5-0.6, GPU offload max, `ollama ps` must show 100% GPU.

## Qwen vs Gemma (r/LocalLLaMA Jun 2026)

- Qwen wins 5/8 shared benchmarks despite smaller footprint, lighter KV cache.
- Split: Qwen for coding/tool-calling/routines/reasoning. Gemma for writing/emails/transcripts/OCR/summarization.
- Video head-to-head (16GB VRAM, browser coding): Gemma 4 12B won UI rounds vs Qwen3.5 9B.
- Practical advice: use both, swap as needed. Qwen3.5 9B at Q8 beats Qwen3.6 at Q4 for some users.

## Qwen3.8-27B (Aug 14 2026)

- Best overall local LLM Sep 2026: 89.2% GPQA, 61.7% SWE-bench Pro, 90.3 LiveCodeBench v6, 73.0 Terminal-Bench 2.1.
- 17.7GB weights, needs 24GB+ free / 32GB Mac. NOT for M1 16GB (<1-7 tok/s, swap, stalls).
- 331-GGUF benchmark on M4 16GB: every 27B+ dense thrashes (>10s TTFT, <0.1 tok/s).

## MLX vs GGUF on M1 (famstack.dev Mar 2026)

- `qwen3.5:9b` GGUF 6.6GB vs `qwen3.5:9b-mlx` 8.9GB.
- M1/M2 lack bf16 -> MLX prefill emulated, GGUF fp16 native.
- Qwen3.5 gated delta-net hybrid attention better in llama.cpp than MLX.
- Broken prompt caching for Qwen3.5 multimodal in some MLX runtimes (LM Studio).
- Ollama ~37% slower than raw llama.cpp/LM Studio GGUF on same engine (Go wrapper overhead).
- oMLX beats both with tiered KV cache, but needs fp16 convert on M1/M2.
- Verdict for M1: GGUF via Ollama is safer. MLX wins on M4/M5 (+37-53%).

## Sources

- r/LocalLLaMA: M1 Pro 16GB usable configs, Qwen3.5 9B agent results, 331-model M4 16GB bench, Gemma4 vs Qwen3.5 benches
- r/LocalLLM: 16GB Apple Silicon model choice, MacBook Air 16GB coding threads
- r/ollama: M4 mini Qwen3/Llama3.1/Qwen2.5 coding benchmark (19-22 tok/s local vs 136 tok/s GPT-4o)
- benchlm.ai, promptquorum.com, agenticwire.news (Sep 2026 tier picks), willitrunai.com (M1 fit list)
- famstack.dev MLX vs GGUF parts 1-2, rapidmlx.com M3 Ultra bench
