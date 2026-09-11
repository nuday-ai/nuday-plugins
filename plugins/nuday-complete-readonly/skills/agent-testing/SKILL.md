---
name: agent-testing
description: Test a NuDay agent by sending it real messages and inspecting the reply,
  right after building or configuring it. Use to verify an agent works — its prompt,
  tools, knowledge, and LLM — before sharing it with users.
metadata:
  source: nuday
  catalog: platform
  category: agent-building
  priority: '5'
---

# Agent Testing

## Overview
After you build or change an agent (see [[nuday-agent-builder]]), test it
before handing it off. This skill uses the NuDay Manager MCP server to query a
live agent and check that its prompt, tools, knowledge bases, and LLM all
behave as intended.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_agents_list` | Find the agent's id |
| `nuday_resolved_config` | Inspect the fully merged (inherited) config |
| `nuday_query_agent` | Send a message to the agent and get its reply |

## Workflow

### 1. Sanity-check the config
Call `nuday_resolved_config` for the agent and confirm it actually has what you
expect: a resolvable LLM, the intended tools/skills/guardrails, and any
`rag_collections`. A missing LLM is the #1 cause of a non-responding agent.

### 2. Query it
```
nuday_query_agent(agent_id="<id>", message="<a representative question>")
```
It resolves the agent's full config server-side and runs it through the
chat worker, returning `{message, thread_id, user_message_id, message_id,
trace_id}`. Pass the same `thread_id` back to test multi-turn memory. It
waits up to `wait_seconds` (default and max 150): a longer run answers
`{"status": "running", "thread_id": ...}` — the run continues server-side,
so re-call with that `thread_id` or read
`GET /api/agent-threads/{thread_id}/history`. Every error reply carries the
ids too.

### 3. Test what matters
- **Tools/RAG**: ask something that *requires* a tool call or a knowledge
  base lookup — confirm the answer reflects it (not a generic guess).
- **Guardrails**: send an input that should be blocked and confirm it is.
- **Persona/format**: check tone and output format match the system prompt.
- **Edge cases**: empty/ambiguous questions, out-of-scope requests.

### 4. Diagnose failures
- Empty/odd replies → re-check `nuday_resolved_config` (LLM, prompt).
- A tool didn't fire → confirm it's attached and its description tells the
  model when to use it; test the tool directly with the
  [[secure-tools-management]] skill (`nuday_test_secure_tool`).
- Use the returned `trace_id` to open the trace in observability for a full
  step-by-step view.

## Best practices
- Test immediately after each change — tight loops beat big-bang testing.
- Use realistic prompts a real user would send, not just "hello".
- Querying consumes LLM tokens and runs the real agent — keep test runs
  purposeful.
