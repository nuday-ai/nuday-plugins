---
name: testing-strategy
description: Create comprehensive testing strategies and write tests. Use when designing
  test suites, writing unit tests, integration tests, or end-to-end tests.
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '12'
---

# Testing Strategy

## Overview
This skill helps create comprehensive testing strategies and write effective tests.

## Test Types

### Unit Tests
- Test individual functions/methods in isolation
- Mock external dependencies
- Aim for high coverage of business logic
- Follow the AAA pattern: Arrange, Act, Assert

### Integration Tests
- Test component interactions
- Verify API contracts
- Test database operations
- Check external service integrations

### End-to-End Tests
- Test complete user workflows
- Simulate real user behavior
- Verify critical business paths
- Keep focused on happy paths and key error scenarios

## Best Practices

### Test Structure
```
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should do expected behavior when given condition', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

### Naming Conventions
- Use descriptive test names
- Start with "should" or "when"
- Describe the expected outcome

### Coverage Guidelines
- Aim for 80%+ coverage on business logic
- Focus on critical paths
- Don't test trivial code
- Cover edge cases and error conditions

## Test Data Management
- Use factories for test data
- Keep test data realistic
- Clean up after tests
- Avoid test interdependencies
