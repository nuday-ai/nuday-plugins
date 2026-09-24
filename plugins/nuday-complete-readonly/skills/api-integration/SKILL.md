---
name: api-integration
description: Integrate with external APIs and services. Use when connecting to REST
  APIs, handling authentication, or processing API responses.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '30'
---

# API Integration

Work from the API's current documentation for endpoints, the auth scheme, rate limits,
pagination and error format, and use its official SDK when there is one.

Make calls robust: set timeouts; retry only idempotent requests and server or
rate-limit errors, with backoff that respects Retry-After; and follow pagination so
results aren't silently truncated. Validate a response's shape before relying on it.

Keep credentials out of code and logs: read them from the environment or a secret
store, and redact them from any output.
