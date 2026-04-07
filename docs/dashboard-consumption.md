# Dashboard Consumption Interfaces

This document defines approved dashboard-facing query interfaces for core analytics outputs.

## Approved Models

1. `dashboard_top_movies_monthly`
- Use-case: top movies by month.
- Grain: one row per `month_start` and `movie_id` (ranked top list from curated mart aggregate).

2. `dashboard_engagement_daily`
- Use-case: daily engagement tracking by movie.
- Grain: one row per `date_key` and `movie_id`.

3. `dashboard_genre_trend_daily`
- Use-case: daily genre trend charts.
- Grain: one row per `date_key` and `genre_id`.

4. `dashboard_rating_distribution`
- Use-case: rating distribution panels.
- Grain: one row per `rating_bucket`.

## Contract Alignment

- All interfaces are sourced from contract-compliant marts and aggregates.
- No downstream team should re-implement upstream transformations.
- Schema changes to these interfaces must follow MART contract versioning policy.
