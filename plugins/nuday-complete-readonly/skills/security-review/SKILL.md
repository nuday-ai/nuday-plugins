---
name: security-review
description: Perform security reviews and vulnerability assessments. Use when auditing
  code for security issues, reviewing authentication, or checking for common vulnerabilities.
metadata:
  source: nuday
  catalog: platform
  category: security
  priority: '8'
---

# Security Review

Approach the code the way an attacker would: find where untrusted input enters
(requests, files, headers, third-party data) and follow it to where it is used, such
as queries, shell commands, file paths, HTML output, deserialization and outbound
requests. Check authentication and authorization on every sensitive action, including
that one user can't reach another's data by changing an id. Look for secrets in code
or logs, weak cryptography or password hashing, and dependencies with known
vulnerabilities.

Report only issues you can point to in the code, with the location, how it could be
exploited, and a concrete fix. Rate each one:
1. **Critical**: fix immediately
2. **High**: fix before deployment
3. **Medium**: fix soon
4. **Low**: consider fixing
5. **Informational**: hardening suggestions
