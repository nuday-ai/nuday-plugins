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

Match the project's existing tests: find how current tests are organized, named and
run (framework, fixtures, mocking style, where test files live) and write new ones
the same way. Don't introduce a new framework or a coverage target unless asked.

Test behavior through public interfaces rather than implementation details, so tests
survive refactoring. Cover what matters most: the business logic, and the edge and
error cases the change touches. A few meaningful tests beat many trivial ones. Keep
tests independent of each other and of run order, and make each failure point at what
broke.

When asked for a strategy rather than tests, say which behaviors belong at the unit,
integration and end-to-end levels for this system, and why. Run the tests you write
when you can, and report the result.
