---
name: sql-assistant
description: Write and optimize SQL queries. Use when creating database queries, optimizing
  performance, or designing schemas.
metadata:
  source: nuday
  catalog: platform
  category: data
  priority: '28'
---

# SQL Assistant

Find out which database and version the query targets, since syntax and optimizer
behavior differ between PostgreSQL, MySQL, SQL Server, SQLite and others, and use the
actual schema rather than guessing table and column names.

Write readable queries: explicit column lists, meaningful aliases, CTEs for multi-step
logic. Pass any user-supplied value as a parameter, never by string concatenation.

For performance, reason from the query plan (EXPLAIN / EXPLAIN ANALYZE) and the
existing indexes rather than rules of thumb, and explain the trade-off of any index you
suggest. Before running anything that changes data (UPDATE, DELETE, schema changes),
show which rows it will affect, for example with a SELECT using the same WHERE
clause.
