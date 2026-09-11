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

## Overview
This skill helps integrate with external APIs effectively and securely.

## Integration Process

### 1. API Assessment
- Review API documentation
- Understand rate limits
- Check authentication requirements
- Identify available endpoints

### 2. Authentication

#### API Keys
```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

#### OAuth 2.0
```python
# Token refresh flow
def refresh_token(refresh_token):
    response = requests.post(token_url, data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id
    })
    return response.json()["access_token"]
```

### 3. Request Handling

#### Best Practices
- Use connection pooling
- Implement retry logic with backoff
- Set appropriate timeouts
- Handle rate limiting gracefully

#### Error Handling
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    # Handle timeout
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        # Handle rate limit
    elif e.response.status_code >= 500:
        # Retry server errors
```

### 4. Response Processing
- Validate response schema
- Handle pagination
- Parse errors appropriately
- Log relevant details

### 5. Security Considerations
- Never log credentials
- Use environment variables for secrets
- Validate SSL certificates
- Sanitize user input in requests
