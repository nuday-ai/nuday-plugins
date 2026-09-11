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

## Overview
This skill helps write efficient SQL queries and design database schemas.

## Query Writing

### SELECT Queries
```sql
SELECT
    column1,
    column2,
    aggregate_function(column3) as alias
FROM table_name
WHERE condition
GROUP BY column1, column2
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

### Best Practices
- Use explicit column names (avoid SELECT *)
- Alias complex expressions
- Use table aliases for joins
- Prefer JOINs over subqueries when possible
- Use CTEs for complex queries

## Query Optimization

### Index Usage
- Ensure WHERE columns are indexed
- Consider composite indexes
- Check index selectivity
- Avoid functions on indexed columns

### Performance Tips
- Limit result sets early
- Use EXPLAIN ANALYZE
- Avoid SELECT DISTINCT when possible
- Optimize JOINs (smaller table first)
- Use appropriate data types

## Common Patterns

### Window Functions
```sql
SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY date DESC) as rn
FROM table_name;
```

### CTEs
```sql
WITH ranked_data AS (
    SELECT *, ROW_NUMBER() OVER (...) as rn
    FROM table_name
)
SELECT * FROM ranked_data WHERE rn = 1;
```

## Schema Design
- Normalize to 3NF typically
- Denormalize for read-heavy workloads
- Use appropriate constraints
- Consider partitioning for large tables
