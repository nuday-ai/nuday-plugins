---
name: technical-documentation
description: Create clear technical documentation including READMEs, API docs, and
  architecture guides. Use when documenting code, APIs, systems, or processes.
metadata:
  source: nuday
  catalog: platform
  category: documentation
  priority: '20'
---

# Technical Documentation

Write for a specific reader and task: decide who will read this (a new user, an API
consumer, a maintainer) and what they need to do, and give them that first. Follow the
structure and tone of the project's existing docs.

- A README lets a newcomer understand what the project is and get it running; setup
  steps must be complete and copy-pasteable.
- API docs give, per endpoint or function: what it does, its parameters, the response
  shape with an example, errors, and auth requirements.
- Architecture docs explain the components, how data flows between them, and why the
  design is the way it is.

Use examples that work against the current code, and define terms the reader may not
know. Keep docs next to the code they describe so they change together.
