---
name: github
description: Browse repositories, read files, search code, and manage issues and pull
  requests on GitHub via the GitHub connector (MCP). Use when the user wants to explore
  a repo, triage or file issues, comment on work, or review pull requests.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '43'
---

# GitHub Connector

## Overview
The GitHub MCP server lets you act on GitHub on the user's behalf, using
the account they connected on the **Providers** page (OAuth). All calls run
as that user, so you only see what they can see.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `list_orgs` | List organizations the user belongs to |
| `list_repos` | List repositories (the user's, or an org's) |
| `get_repo` | Repository details (default branch, visibility, description) |
| `list_branches` | List a repo's branches |
| `get_file_contents` | Read a file (or list a directory) at a path/ref |
| `search_code` | Search code across repositories with a query |
| `list_issues` | List issues in a repo (filter by state/labels) |
| `get_issue` | Full issue details + body |
| `create_issue` | Open a new issue (title, body, labels) |
| `update_issue` | Edit an issue — title, body, labels, or close it |
| `add_issue_comment` | Comment on an issue or pull request |
| `list_pull_requests` | List PRs in a repo (filter by state) |
| `get_pull_request` | PR details — branches, state, mergeability |

> Read/triage oriented: you can read PRs and comment on them, but creating
> or merging PRs and pushing commits are **not** exposed here — do those in
> the GitHub UI or via the `av` CLI / git in a workspace.

## Common recipes

**Explore a repo**
1. `get_repo` for the default branch + description.
2. `get_file_contents` on `README.md` (and the path the user names).
3. `list_branches` if they ask what's in flight.

**Find code**
- `search_code` with a focused query (e.g. `repo:owner/name authenticate`).
  Narrow queries return better results — include `repo:`/`path:`/`language:`
  qualifiers when you can.

**Triage / file an issue**
1. `list_issues` (state `open`) to check for duplicates first.
2. `create_issue` with a clear title and a body that states context,
   expected vs. actual, and repro steps. Add labels when known.
3. To follow up: `add_issue_comment`; to resolve: `update_issue` (set
   `state: closed`).

**Review a pull request**
1. `get_pull_request` for state + the head/base branches.
2. `get_file_contents` at the head ref to read changed files.
3. `add_issue_comment` on the PR number to leave review notes.

## Best practices
- Reference issues/PRs by `#number`; show commit SHAs in short form (first 7).
- Link to the GitHub web UI when pointing at a specific item.
- Format code in fenced blocks with the language identifier.
- Confirm before opening/closing issues or posting public comments — these
  are outward-facing writes.

## Error handling
- If nothing comes back / auth fails, the user likely hasn't connected
  GitHub — point them to the **Providers** page to connect.
- "Not found" on a repo usually means it's private or misspelled, not gone.
- Respect rate limits — GitHub's API is capped per hour.
