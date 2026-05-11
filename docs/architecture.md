# Architecture

## Purpose

`dbt-search-observatory` is designed as a local analytics engineering artifact for search and crawl telemetry. Instead of assuming a production warehouse account, it packages realistic seeds and a DuckDB profile so the project can be run entirely from the repo.

## Modeling Shape

### Raw Inputs

- `search_console_daily`
- `crawl_observations`
- `url_inventory`

### Staging

- `stg_search_console_daily`
- `stg_crawl_observations`
- `stg_url_inventory`

### Marts

- `mart_url_observability`
- `mart_page_group_performance`
- `mart_anomaly_flags`
- `mart_site_health`

## Design Notes

- The warehouse is intentionally local-first to avoid setup drag.
- dbt tests focus on relationships, uniqueness, and accepted values.
- The anomaly layer is simple but operator-facing: it produces concrete issue classes and next actions rather than only KPI summaries.
- Screenshot proof is generated from the built DuckDB state, not from hand-edited mock files.

## Why DuckDB

DuckDB keeps the repo:

- self-contained
- credential-free
- fast to validate in CI
- easy to inspect locally

## Extension Paths

- swap DuckDB for Postgres, BigQuery, or Snowflake via dbt profile changes
- add incremental ingestion or snapshot history
- add exposure definitions and dbt docs site publishing
- layer in freshness SLA policies for crawl/index lag
