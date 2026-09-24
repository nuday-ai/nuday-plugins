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

Review the change against what it is trying to do: read the description or linked
issue first, then the diff, and read surrounding code wherever the diff alone doesn't
show whether something is correct. Judge it by the conventions this codebase already
follows rather than a generic style guide.

Put correctness first (bugs, missed edge cases, broken error handling, security
problems such as injection or leaked credentials), then design and maintainability,
then style. Point to the exact file and line, say why it matters, and suggest a fix.
When something is fine, say so plainly rather than padding the review with nits.

Group feedback as:
1. **Critical issues**: must be fixed before merge
2. **Suggestions**: would improve the code
3. **Questions**: things you need clarified
4. **Praise**: what was done well
