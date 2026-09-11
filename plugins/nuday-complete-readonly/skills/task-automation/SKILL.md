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

## Overview
This skill helps create efficient automated workflows and scripts.

## Automation Principles

### When to Automate
- Task is performed frequently
- Task is well-defined and repeatable
- Manual execution is error-prone
- Time savings outweigh setup cost

### Automation Design
1. **Identify**: What needs automating?
2. **Document**: Write down manual steps
3. **Design**: Plan the automation flow
4. **Implement**: Build incrementally
5. **Test**: Verify all scenarios
6. **Monitor**: Track execution and errors

## Script Patterns

### Bash Script Template
```bash
#!/bin/bash
set -euo pipefail

# Configuration
LOG_FILE="/var/log/automation.log"
LOCK_FILE="/tmp/automation.lock"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Cleanup on exit
cleanup() {
    rm -f "$LOCK_FILE"
    log "Script completed"
}
trap cleanup EXIT

# Prevent concurrent execution
if [ -f "$LOCK_FILE" ]; then
    log "ERROR: Script already running"
    exit 1
fi
touch "$LOCK_FILE"

# Main logic
main() {
    log "Starting automation..."
    # Your automation steps here
}

main "$@"
```

### Python Script Template
```python
#!/usr/bin/env python3
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting automation...")
    try:
        # Your automation logic here
        pass
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        sys.exit(1)
    logger.info("Automation completed successfully")

if __name__ == "__main__":
    main()
```

## Best Practices
- Include error handling
- Add logging for debugging
- Use configuration files
- Implement dry-run mode
- Add notification on failure
- Document dependencies
