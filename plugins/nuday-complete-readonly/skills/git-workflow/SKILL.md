---
name: git-workflow
description: Manage Git workflows and version control. Use when working with branches,
  reviewing commits, resolving conflicts, or managing releases.
metadata:
  source: nuday
  catalog: platform
  category: devops
  priority: '35'
---

# Git Workflow

## Overview
This skill helps manage Git workflows and version control best practices.

## Branching Strategy

### Git Flow
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Production fixes

### Branch Naming
```
feature/AV-123-add-user-auth
bugfix/AV-456-fix-login-error
hotfix/AV-789-critical-security-fix
```

## Commit Messages

### Format
```
type(scope): subject

body (optional)

footer (optional)
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples
```
feat(auth): add OAuth2 support

Implements OAuth2 authentication flow with:
- Google provider
- Token refresh logic
- Session management

Closes #123
```

## Common Operations

### Rebasing
```bash
git fetch origin
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease
```

### Squashing
```bash
git rebase -i HEAD~3
# Change 'pick' to 'squash' for commits to combine
```

### Cherry-picking
```bash
git cherry-pick <commit-hash>
```

## Best Practices
- Commit early and often
- Keep commits focused and atomic
- Write meaningful commit messages
- Review before pushing
- Never force push to shared branches
- Use pull requests for collaboration
