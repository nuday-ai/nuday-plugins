---
name: agent-evaluations
description: Evaluate agents via the NuDay Evaluations MCP server — run a suite of
  scored test cases against an agent and poll the results. Use to measure an agent's
  quality, and to A/B compare changes.
metadata:
  source: nuday
  catalog: platform
  category: agent-building
  priority: '6'
---

# Agent Evaluations

## Overview
Quality capability via the **NuDay Evaluations** MCP
server. Use it to prove an agent is good before shipping —
after building it with [[nuday-agent-builder]] and smoke-testing it with
[[agent-testing]].

- **Evaluations** — run a suite of test cases against an agent; each case is
  scored by assertions (deterministic + LLM-as-judge). Good for regression
  testing and A/B comparing prompt/model changes.

Evaluations run as background jobs — you get a `run_id` and poll for results.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_assertion_types` | The assertion types you can use in test cases |
| `nuday_run_evaluation` | Run a test-case suite against an agent → `run_id` |
| `nuday_get_evaluation_run` | Poll status + pass rates + per-test outcomes |
| `nuday_list_evaluation_runs` | Recent eval runs (newest first) |

## Evaluating an agent

### 1. Write test cases
Check `nuday_list_assertion_types`, then build a JSON array. Each case has an
`input`, an optional `expected` reference, and `assertions`:
```json
[
  {"input": "What is our refund window?",
   "assertions": [{"type": "contains", "value": "30 days"},
                  {"type": "max-latency", "value": "8000"}]},
  {"input": "Summarize the SLA.",
   "assertions": [{"type": "llm-rubric",
                   "value": "Mentions uptime % and support response time"}]}
]
```
Common assertion types: `contains` / `icontains` / `not-contains`, `equals`,
`regex`, `is-json`, `min-length` / `max-length`, `max-latency` (deterministic);
`llm-rubric`, `answer-relevance`, `factuality` (LLM-graded, 0–1 score).

### 2. Run + poll
```
run_evaluation(agent_id="<id>", test_cases="<json>", repeat_count=3)
```
`repeat_count` (1–10) runs each case multiple times to catch flakiness. Then
poll `get_evaluation_run(run_id)` until `status` is `completed`; read
`overall_pass_rate` and per-config `metrics` (pass rate, latency, tokens).

### 3. A/B compare (optional)
Run the same suite before and after a change and compare pass rates /
latency. (The UI supports multi-config runs in one go; via MCP, run each
variant and compare the results.)

## Best practices
- Cover the behaviors that matter: correctness, format, refusals/guardrails,
  and edge cases — not just the happy path.
- Prefer deterministic assertions where you can; reserve `llm-rubric` for
  judgments that genuinely need a model.
- Evaluations consume LLM tokens and run the real target — keep
  suites focused and use `repeat_count` deliberately.
- Re-run the same suite after every change to catch regressions.
