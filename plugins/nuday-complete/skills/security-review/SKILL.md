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

## Overview
This skill helps identify and address security vulnerabilities in code and systems.

## Security Checklist

### Authentication & Authorization
- [ ] Passwords properly hashed (bcrypt, argon2)
- [ ] Session management secure
- [ ] MFA available for sensitive operations
- [ ] Principle of least privilege applied
- [ ] API keys not exposed in code

### Input Validation
- [ ] All user input validated
- [ ] Input sanitized before use
- [ ] Parameterized queries used
- [ ] File upload restrictions in place
- [ ] Content-Type headers verified

### Common Vulnerabilities

#### SQL Injection
```python
# BAD
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

#### XSS (Cross-Site Scripting)
- Escape HTML output
- Use Content-Security-Policy
- Validate URL parameters
- Sanitize rich text input

#### CSRF (Cross-Site Request Forgery)
- Use CSRF tokens
- Verify Origin header
- Use SameSite cookies

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS for data in transit
- [ ] PII properly handled
- [ ] Secrets in environment variables
- [ ] Logs don't contain sensitive data

### Infrastructure
- [ ] Minimal ports exposed
- [ ] Security headers configured
- [ ] Dependencies updated
- [ ] Error messages non-revealing

## Output Format
Provide findings as:
1. **Critical**: Must fix immediately
2. **High**: Fix before deployment
3. **Medium**: Address soon
4. **Low**: Consider fixing
5. **Informational**: Best practice suggestions
