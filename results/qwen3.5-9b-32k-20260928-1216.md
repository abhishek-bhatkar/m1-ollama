# bench-suite qwen3.5-9b-32k (20260928-1216)
ps-before:
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL

L0a-chat-exact: PASS reply='LOCAL OK' wall=7.2s
L0b-chat-story: PASS tokens=34 tok/s=9.9 wall=4.0s
L1-edit-sample: PASS tok/s=10.0 wall=2.4s
L2-agent: running `opencode run --model ollama-local/qwen3.5-9b-32k Reply with exactly: T3 OK` in scratch dir (timeout 120s)...
L2-agent: FAIL (timeout after 120s, no converging answer - see docs/REALWORLD.md)
ps-after:
NAME                     ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
qwen3.5-9b-32k:latest    b8ff5e20d206    6.1 GB    100% GPU     32768      4 minutes from now
Rule: agent usable only if L2 passes twice in a row.
