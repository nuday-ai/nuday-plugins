---
name: knowledge-base-management
description: Create, populate, query, and delete Knowledge Bases (RAG collections)
  via the NuDay Manager MCP server. Use when an agent needs to set up retrieval-augmented
  generation — build a knowledge base, ingest text into it, then attach it to an agent
  for grounded answers.
metadata:
  source: nuday
  catalog: platform
  category: data
  priority: '6'
---

# Knowledge Base (RAG) Management

## Overview
A **Knowledge Base** (RAG collection) is a vector store an agent can search
to ground its answers in your content. This skill covers the lifecycle —
create, ingest, inspect, delete — via the NuDay Manager MCP server. To make an
agent actually use a KB, attach its id under `rag_collections` with the
[[nuday-agent-builder]] skill.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_knowledge_bases` | Browse knowledge bases (optional `query`) |
| `nuday_get_knowledge_base` | Details + embedding/chunking config |
| `nuday_create_knowledge_base` | Create a new KB (provisions the vector store) |
| `nuday_ingest_text` | Chunk + embed a block of text into a KB |
| `nuday_delete_knowledge_base` | Delete a KB, its table, and its LDAP groups |

## Workflow

### 1. Create
`nuday_create_knowledge_base(name=..., description=...)`. Optional `chunk_size`
(default 1000) and `chunk_overlap` (default 200) tune retrieval granularity:
smaller chunks = more precise hits, larger = more context per hit. It
provisions a Postgres vector table and inherits the tenant's embedding
config. Note the returned `id`.

### 2. Ingest content
Call `nuday_ingest_text(collection_id=..., text=..., source_name="...")` for
each piece of content (notes, fetched web pages, generated material). The
text is chunked, embedded, and stored; `source_name` is a label (an
extension is added automatically). Returns the number of chunks stored.
- For large or many **files**, use the manager UI / upload API instead —
  `nuday_ingest_text` is for text you already have in hand.

### 3. Verify
`nuday_get_knowledge_base(collection_id)` shows `chunk_count` / `doc_count` and
`status` (`ready` once ingestion finishes).

### 4. Attach to an agent
Add the KB id to the agent's `rag_collections` via `nuday_agent_configure`
(see [[nuday-agent-builder]]). Then [[agent-testing]] confirms the agent
actually retrieves from it.

### 5. Delete (careful)
`nuday_delete_knowledge_base(collection_id)` drops the vector table and LDAP
groups — irreversible. Only the creator or a tenant admin (CAN_MANAGE) may
delete; system knowledge bases cannot be deleted.

## Best practices
- Ingest clean, deduplicated text — garbage in, garbage retrieved.
- Give each source a meaningful `source_name`; it travels into chunk
  metadata and helps trace where an answer came from.
- Keep one KB per coherent topic/corpus rather than one giant mixed bag.
- Confirm `status: ready` before relying on retrieval.

## Tenancy
`nuday_create_knowledge_base` also accepts `tenant_id` (a tenancy you belong
to; `nuday_whoami` lists them) when you have no active tenancy, and
`embedding_entity_id` to pin the embedding backend/provider it resolves.
