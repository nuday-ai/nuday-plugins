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

Follow the conventions this repository already uses rather than imposing a
branching model or commit format. Before branching or committing, read
`git log --oneline -20` and the branch list to see how the repo names
branches and writes commit messages, and match them. A CONTRIBUTING file or
commit template in the repo takes precedence.

Some Git operations are hard to undo:
- Never force-push to a shared branch (main, a release branch, or someone
  else's branch). On your own branch, use `--force-with-lease`.
- Don't rewrite history that has already been pushed and shared.

Keep each commit to one logical change, and review `git diff --staged`
before committing.
