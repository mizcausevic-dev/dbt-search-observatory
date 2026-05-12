# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-12

### Released
- Published **dbt-search-observatory** as a public, portfolio-grade system focused on ai retrieval reliability.
- Packaged the current implementation, documentation, validation flow, and proof surfaces into a repo that can be reviewed by technical and operating stakeholders.
- Clarified the core problem the project is addressing: retrieval drift, citation breakdowns, and rising hallucination risk as corpora and prompts evolve.

### Why this mattered
- Existing approaches in vector tooling, LLM observability stacks, and evaluation suites were useful for parts of the workflow.
- They still left out a durable operator workflow for evidence quality, source freshness, and trust decisions.
- This release made the repo read like an operational capability rather than a narrow technical demo.

## [0.1.0] - 2026-01-09

### Shipped
- Cut the first coherent internal version of **dbt-search-observatory** with stable domain objects, review surfaces, and decision outputs.
- Established the first reviewable version of the architecture described as: dbt + DuckDB warehouse for search console, crawl, index coverage, freshness drift, and URL-level observability diagnostics.
- Focused the repo around actionability instead of passive reporting.

## [Prototype] - 2025-04-18

### Built
- Built the first runnable prototype for the repo's main workflow and decision model.
- Validated the concept against pressure points such as RAG hallucination rates, stale retrieval context, and citation-quality breakdowns.
- Used the prototype phase to test whether the project could drive action, not just present information.

## [Design Phase] - 2024-07-16

### Designed
- Defined the system around operator-first and decision-legible outputs.
- Chose interfaces and examples that made sense for AI platform, search, and knowledge-system teams.
- Avoided reducing the project to a generic dashboard, CRUD app, or fashionable wrapper around the stack.

## [Idea Origin] - 2024-01-16

### Observed
- The original idea surfaced while looking at how teams were handling retrieval drift, citation breakdowns, and rising hallucination risk as corpora and prompts evolve.
- The recurring pattern was that teams had data and tools, but still lacked a usable operating layer for the hardest decisions.

## [Background Signals] - 2022-08-09

### Context
- Earlier platform, governance, and operator-tooling work made one pattern hard to ignore: the systems that create the most drag are often the ones with partial controls and weak operational coherence, not the ones with no controls at all.
- That pattern shaped the thinking behind this repo well before the public version existed.