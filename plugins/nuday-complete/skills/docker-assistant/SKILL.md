---
name: docker-assistant
description: Create and manage Docker containers and compose files. Use when containerizing
  applications, writing Dockerfiles, or managing multi-container setups.
metadata:
  source: nuday
  catalog: platform
  category: devops
  priority: '38'
---

# Docker Assistant

Follow the project's existing Dockerfile and compose conventions where they exist. For
new images:
- Pin base images to a specific version tag, and prefer slim variants.
- Order layers so rarely changing steps (installing dependencies) come before
  frequently changing ones (copying source), and use multi-stage builds to keep build
  tools out of the final image.
- Run as a non-root user. Keep secrets out of the image: pass them at runtime, not
  through ENV or build args, which are stored in the image layers.
- Add a .dockerignore so local files, VCS data and secrets stay out of the build.

Use Docker Compose v2 syntax; the top-level `version:` key is obsolete and can be
omitted.
