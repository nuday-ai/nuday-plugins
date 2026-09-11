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

## Overview
This skill helps create efficient Docker configurations and manage containers.

## Dockerfile Best Practices

### Multi-stage Build
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Optimization Tips
- Use specific base image tags
- Order layers by change frequency
- Minimize layers with combined RUN commands
- Use .dockerignore
- Don't run as root

### Security
```dockerfile
# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

## Docker Compose

### Basic Structure
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password

volumes:
  postgres_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Common Commands
```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f app

# Execute command in container
docker compose exec app sh

# Clean up
docker compose down -v
```
