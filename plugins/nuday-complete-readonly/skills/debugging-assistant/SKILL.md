---
name: debugging-assistant
description: Systematic debugging and troubleshooting. Use when investigating bugs,
  analyzing error logs, or diagnosing issues in applications.
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '15'
---

# Debugging Assistant

Find the cause before proposing a fix. Start from the evidence (the exact error, stack
trace, logs and steps to reproduce) and ask for what's missing rather than guessing.
Reproduce the problem if you can, then narrow it down (recent changes, the smallest
failing input, bisecting) until you can explain why it happens.

Fix the root cause with the smallest change that does it rather than suppressing the
symptom, and add a regression test when the codebase has tests.

Report:
1. The likely root cause, and how confident you are
2. How to verify it
3. The fix
4. How to prevent it recurring, if there's something worth changing
