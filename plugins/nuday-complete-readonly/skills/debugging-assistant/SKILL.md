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

## Overview
This skill provides systematic debugging and troubleshooting guidance.

## Debugging Process

### 1. Reproduce the Issue
- Gather steps to reproduce
- Identify consistent patterns
- Note environment details
- Document expected vs actual behavior

### 2. Isolate the Problem
- Narrow down the affected code
- Use binary search approach
- Check recent changes
- Verify input data

### 3. Analyze Root Cause
- Review stack traces
- Check error logs
- Examine application state
- Trace data flow

### 4. Common Issue Types

#### Logic Errors
- Off-by-one errors
- Incorrect conditionals
- Missing null checks
- Race conditions

#### Integration Issues
- API contract mismatches
- Authentication failures
- Network timeouts
- Data format inconsistencies

#### Performance Issues
- Memory leaks
- N+1 queries
- Blocking operations
- Resource exhaustion

### 5. Resolution
- Implement fix with minimal scope
- Add regression tests
- Document the root cause
- Update monitoring if needed

## Debug Output
When debugging, provide:
1. Likely root cause(s)
2. Steps to verify
3. Suggested fix
4. Prevention recommendations
