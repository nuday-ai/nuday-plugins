---
name: skill-creator
description: Create new agent skills following the Agent Skills specification
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '30'
---

# Skill Creator

## Overview
Meta-skill for creating new skills that conform to the Agent Skills specification (agentskills.io).

## Skill structure

A skill is a folder with this layout:

```
my-skill/
  SKILL.md          # Required — the instruction document
  scripts/          # Optional — bundled helper scripts
    helper.py
  references/       # Optional — reference documents
    api-spec.md
  assets/           # Optional — static assets
    template.json
  metadata.json     # Optional — machine-readable metadata
```

## SKILL.md format

```markdown
# Skill Name

## Overview
One-paragraph description of what the skill does and when to use it.

## Usage
Step-by-step instructions or code examples.

## Capabilities
Bullet list of what the skill can do.

## Guidelines
Numbered list of best practices and constraints.
```

## metadata.json format

```json
{
  "name": "my-skill",
  "description": "Short description",
  "category": "development",
  "tags": ["tag1", "tag2"],
  "priority": 50,
  "scripts": ["scripts/helper.py"],
  "references": ["references/api-spec.md"],
  "assets": ["assets/template.json"]
}
```

## Steps to create a skill

1. **Choose a name** — lowercase, hyphens only (e.g., `data-pipeline`).
2. **Pick a category** — one of: development, documentation, creative, communication, data, integration, automation, security, devops, domain, custom.
3. **Write SKILL.md** — follow the format above. Be specific and actionable.
4. **Add scripts** (optional) — small, self-contained helpers. Include a shebang line and argparse for CLI usage.
5. **Add references** (optional) — API docs, schemas, or examples the skill needs.
6. **Add assets** (optional) — templates, config files, or static resources.
7. **Register the skill** — POST to the skills API or use the `av` CLI:
   ```bash
   av skills create --from-folder ./my-skill/
   ```

## Guidelines
1. Keep instruction text focused — one skill, one job.
2. Scripts should be runnable standalone (`python script.py --help`).
3. Prefer standard-library or widely-available dependencies.
4. Tag skills generously — tags power discovery.
5. Set priority thoughtfully: 1-10 = critical/always-on, 11-30 = commonly used, 31-70 = on-demand, 71-100 = niche/experimental.
6. Test the skill by loading it into an agent and verifying it produces correct output.
