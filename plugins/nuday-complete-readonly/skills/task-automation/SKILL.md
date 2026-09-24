---
name: task-automation
description: Create automated workflows and scripts. Use when automating repetitive
  tasks, creating scheduled jobs, or building workflow pipelines.
metadata:
  source: nuday
  catalog: platform
  category: automation
  priority: '40'
---

# Task Automation

Before automating, confirm the manual steps and what "done" looks like, and check
whether an existing scheduler or pipeline (cron, CI, this platform's scheduled
automations) already fits.

Scripts that run unattended must be safe to re-run and must fail loudly: make them
idempotent, stop on errors (in bash, `set -euo pipefail`), log what they did, and exit
non-zero on failure so the scheduler notices. Keep configuration and secrets out of
the script. For anything that changes or deletes data, add a dry-run mode and try it
first.
