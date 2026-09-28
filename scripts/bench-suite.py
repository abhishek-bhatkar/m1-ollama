#!/usr/bin/env python3
"""bench-suite: repeatable real-world benchmark for any Ollama model on M1 16GB.

Usage: ./scripts/bench-suite.sh <ollama-model> [opencode-model]
  e.g. ./scripts/bench-suite.sh qwen3.5-9b-32k ollama-local/qwen3.5-9b-32k

Tiers:
  L0-chat  direct Ollama /api/generate, think=false, exact-reply + 40-token story
  L1-edit  direct Ollama, fix fixtures/sample.py (tests reasoning without agent loop)
  L2-agent bounded `opencode run` (120s timeout) on a scratch task.
           Hangs become FAIL instead of hanging you.

Output: results/<model>-<YYYYMMDD-HHMM>.md (this is the cross-model comparison file)
Rule: a model graduates to "agent usable" only if L2 passes twice in a row.
"""
import json, subprocess, sys, time, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
FIXTURE = (ROOT / "scripts" / "fixtures" / "sample.py").read_text()

OLLAMA = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5-9b-32k"
OPENCODE_MODEL = sys.argv[2] if len(sys.argv) > 2 else f"ollama-local/{OLLAMA}"
L2_TIMEOUT = 120
out = []
def log(s): print(s, flush=True); out.append(s)

def ollama_generate(prompt, timeout=180):
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=json.dumps({"model": OLLAMA, "prompt": prompt,
                         "think": False, "stream": False}).encode(),
        headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    dt = time.time() - t
    ec, ed = d.get("eval_count", 0), d.get("eval_duration", 1)
    return d.get("response", ""), ec, ec / (ed / 1e9) if ed else 0, dt

def ollama_ps():
    try:
        return subprocess.run(["ollama", "ps"], capture_output=True,
                              text=True, timeout=15).stdout.strip()
    except Exception as e:
        return f"ollama ps failed: {e}"

ts = datetime.now().strftime("%Y%m%d-%H%M")
log(f"# bench-suite {OLLAMA} ({ts})")
log(f"ps-before:\n{ollama_ps()}\n")

# L0a exact reply
try:
    resp, ec, tps, dt = ollama_generate("Reply with exactly: LOCAL OK")
    ok = "LOCAL OK" in resp
    log(f"L0a-chat-exact: {'PASS' if ok else 'FAIL'} reply={resp.strip()[:60]!r} wall={dt:.1f}s")
except Exception as e:
    log(f"L0a-chat-exact: FAIL error={e}")

# L0b story tok/s
try:
    resp, ec, tps, dt = ollama_generate("Write a 30-word story about a robot.")
    log(f"L0b-chat-story: {'PASS' if ec >= 20 else 'FAIL'} tokens={ec} tok/s={tps:.1f} wall={dt:.1f}s")
except Exception as e:
    log(f"L0b-chat-story: FAIL error={e}")

# L1 single-file edit via API (no agent loop)
try:
    resp, ec, tps, dt = ollama_generate(
        "Fix ONLY the bug in this python (add() subtracts instead of adding). "
        "Reply with the corrected add() function only:\n" + FIXTURE, timeout=240)
    ok = "a + b" in resp or "a+b" in resp
    log(f"L1-edit-sample: {'PASS' if ok else 'FAIL'} tok/s={tps:.1f} wall={dt:.1f}s")
except Exception as e:
    log(f"L1-edit-sample: FAIL error={e}")

# L2 bounded agent run in scratch dir
import tempfile
with tempfile.TemporaryDirectory(prefix="bench-l2-") as td:
    Path(td, "task.txt").write_text("Reply with exactly: T3 OK\n")
    cmd = ["opencode", "run", "--model", OPENCODE_MODEL, "Reply with exactly: T3 OK"]
    log(f"L2-agent: running `{' '.join(cmd)}` in scratch dir (timeout {L2_TIMEOUT}s)...")
    t = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=td, timeout=L2_TIMEOUT)
        dt = time.time() - t
        combined = (p.stdout + p.stderr).strip()
        ok = "T3 OK" in combined and p.returncode == 0
        log(f"L2-agent: {'PASS' if ok else 'FAIL'} rc={p.returncode} wall={dt:.1f}s out={combined[:200]!r}")
    except subprocess.TimeoutExpired:
        log(f"L2-agent: FAIL (timeout after {L2_TIMEOUT}s, no converging answer - see docs/REALWORLD.md)")

log(f"ps-after:\n{ollama_ps()}")
log("Rule: agent usable only if L2 passes twice in a row.")

name = OLLAMA.replace(":", "-").replace("/", "-")
dest = RESULTS / f"{name}-{ts}.md"
dest.write_text("\n".join(out) + "\n")
print(f"\nWrote {dest}")
