---
name: code-review
description: Perform systematic code reviews with best practices. Use when reviewing
  pull requests, examining code quality, or suggesting improvements to existing code.
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '10'
---

# Code Review

## Overview
This skill enables systematic code review following industry best practices.

## Review Process

### 1. Initial Assessment
- Understand the purpose of the changes
- Identify the scope and affected areas
- Check if tests are included

### 2. Code Quality Checks
- **Readability**: Is the code easy to understand?
- **Naming**: Are variables, functions, and classes well-named?
- **Structure**: Is the code well-organized?
- **DRY**: Is there unnecessary duplication?
- **SOLID**: Does the code follow SOLID principles?

### 3. Security Review
- Check for hardcoded secrets or credentials
- Validate input handling and sanitization
- Review authentication and authorization logic
- Look for SQL injection, XSS, and other vulnerabilities

### 4. Performance Considerations
- Identify potential bottlenecks
- Check for unnecessary computations
- Review database queries for efficiency
- Consider memory usage

### 5. Best Practices
- Proper error handling
- Appropriate logging
- Documentation where needed
- Consistent coding style

## Output Format
Provide feedback in structured categories:
1. **Critical Issues**: Must be fixed before merge
2. **Suggestions**: Improvements that would enhance the code
3. **Questions**: Clarifications needed
4. **Praise**: Well-implemented aspects
