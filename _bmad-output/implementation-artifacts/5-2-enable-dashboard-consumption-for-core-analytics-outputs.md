# Story 5.2: Enable Dashboard Consumption for Core Analytics Outputs

Status: done

## Story

As an Analytics Engineer,
I want curated engagement and trend outputs consumable by dashboard tools,
so that reporting can be delivered without re-implementing upstream preparation logic.

## Acceptance Criteria

1. Given contract-compliant marts and aggregates exist, when dashboard consumers query approved datasets, then top movies, engagement, genre trend, and rating distribution use-cases are supported by curated outputs.
2. Given contract-compliant marts and aggregates exist, when dashboard consumers query approved datasets, then query interfaces align with documented dataset semantics.

## Tasks / Subtasks

- [x] Implement minimal curated outputs for core dashboard use-cases (AC: 1)
  - [x] Add `dashboard_top_movies_monthly` based on `agg_top_movies_by_month`.
  - [x] Add `dashboard_engagement_daily` based on `fct_movie_consumption_daily` and `dim_movies`.
  - [x] Add `dashboard_genre_trend_daily` for daily genre trend rollups.
  - [x] Add `dashboard_rating_distribution` for rating bucket distribution.
- [x] Register schema checks for dashboard models (AC: 1)
  - [x] Add `not_null` and relationships tests in marts schema metadata.
- [x] Publish lightweight interface semantics for downstream consumers (AC: 2)
  - [x] Add concise dashboard consumption documentation in `docs/dashboard-consumption.md`.
- [x] Validate dbt parse/build for new models in local environment (AC: 1, 2)
  - [x] Verified with `uv run dbt parse` and `uv run dbt build --select dashboard_top_movies_monthly dashboard_engagement_daily dashboard_genre_trend_daily dashboard_rating_distribution`.

## Dev Agent Record

### Agent Model Used

GPT-5.3-Codex

### Completion Notes List

- Implemented essential-only Story 5.2 scope without overengineering, aligned with user direction.
- Added four dashboard-facing curated dbt models for top movies, engagement, genre trend, and rating distribution.
- Added schema-level tests for dashboard models in marts schema configuration.
- Added downstream query semantics documentation for approved dashboard interfaces.
- Validated successfully using the same working dbt flow as previous epics from `mflix_snowflake/` directory.
- dbt result: PASS=15, WARN=0, ERROR=0, SKIP=0 for all new dashboard models and tests.

### File List

- mflix_snowflake/models/marts/dashboard_engagement_daily.sql
- mflix_snowflake/models/marts/dashboard_top_movies_monthly.sql
- mflix_snowflake/models/marts/dashboard_genre_trend_daily.sql
- mflix_snowflake/models/marts/dashboard_rating_distribution.sql
- mflix_snowflake/models/marts/schema.yml
- docs/dashboard-consumption.md
- _bmad-output/implementation-artifacts/5-2-enable-dashboard-consumption-for-core-analytics-outputs.md

## Change Log

- 2026-04-07: Added minimal curated dashboard outputs and interface semantics docs; validated with dbt parse/build and marked done.
