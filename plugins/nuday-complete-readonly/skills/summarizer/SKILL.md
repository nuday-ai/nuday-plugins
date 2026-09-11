---
name: summarizer
description: Summarize documents and long-form content using multi-pass strategies
metadata:
  source: nuday
  catalog: platform
  category: documentation
  priority: '25'
---

# Summarizer

## Overview
Produce clear, accurate summaries of documents and long-form content. Use a multi-pass strategy to handle documents of any length.

## Strategy

### Pass 1 — Chunked extraction
Split the source into manageable chunks (roughly 3000-4000 words each). For each chunk, extract:
- Key claims and facts
- Named entities (people, orgs, dates, figures)
- Decisions or action items

### Pass 2 — Consolidation
Merge the per-chunk extractions:
1. De-duplicate overlapping facts.
2. Resolve contradictions (prefer later sections if the document is chronological).
3. Group related items under thematic headings.

### Pass 3 — Final summary
Write the summary in the requested format:
- **Executive summary** (1-2 paragraphs): high-level overview for decision-makers.
- **Bullet summary** (5-15 bullets): scannable key points.
- **Detailed summary** (1-2 pages): section-by-section breakdown.

## Output format
Always include at the top:
```
Source: <document name or URL>
Length: <original word count>
Summary type: <executive | bullet | detailed>
```

## Guidelines
1. Preserve factual accuracy — never invent details not in the source.
2. Attribute quantitative claims (e.g., "revenue grew 15% per the Q3 report").
3. Flag areas of ambiguity: "The document is unclear on whether X applies to Y."
4. For multi-document summarization, note which source each fact comes from.
5. Default to **bullet summary** unless the user requests a different format.
6. If the document exceeds context limits, use the chunked extraction strategy above rather than truncating.
