# 🎬 MFlix Analytics Platform - Dagster + dlt + dbt + Snowflake

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Dagster](https://img.shields.io/badge/Orchestration-Dagster-5c6cff.svg)](https://dagster.io/)
[![dlt](https://img.shields.io/badge/Ingestion-dlt-1f7a8c.svg)](https://dlthub.com/)
[![dbt](https://img.shields.io/badge/Transform-dbt-orange.svg)](https://www.getdbt.com/)
[![Soda](https://img.shields.io/badge/Quality-Soda-0ea5e9.svg)](https://www.soda.io/)
[![Snowflake](https://img.shields.io/badge/Warehouse-Snowflake-29b5e8.svg)](https://www.snowflake.com/)
[![uv](https://img.shields.io/badge/Package%20Manager-uv-3f7cff.svg)](https://github.com/astral-sh/uv)

A practical end-to-end data platform for MFlix analytics: MongoDB ingestion, Snowflake warehousing, dbt modeling, Soda quality controls, and Dagster orchestration with end-user outputs for ad-hoc, BI, and simple ML use cases.

## 🖼️ System Architecture

Architecture image:

![MFlix Pipeline Architecture](images/project_architecture.svg)

Source file:

- `excalidraw/mflix-pipeline-architecture.excalidraw` (editable source)

## 🔧 Key Features

- End-to-end ELT: MongoDB -> dlt -> Snowflake -> dbt marts.
- Quality-first pipeline with Soda checks and quality audit logs.
- Contracted marts for stable downstream consumption.
- Dedicated end-user workloads:
  - ad-hoc genre report
  - BI KPI snapshot
  - simple ML monthly rating forecast
- Production-like orchestration using Dagster jobs and schedules.

## 📦 Outputs for End Users

Generated outputs are written to `data/`:

- `data/ad_hoc_genre_interest_report.csv`
- `data/bi_kpi_snapshot.csv`
- `data/ml_monthly_rating_forecast.csv`
- `data/movie_engagement.csv`
- `data/top_movies_by_month.csv`

## 📸 Pipeline Screenshots

Add screenshots here to make README look production-ready:

- `images/dagster_graph.png`
- `images/dagster_jobs_runs.png`
- `images/snowflake_dashboard_output.png`
- `images/soda_quality_output.png`

Screenshot checklist:

- `images/SCREENSHOTS_NEEDED.md`

## 🛠️ Tech Stack Details

| Layer | Tool | Purpose |
| --- | --- | --- |
| Orchestration | Dagster | Assets, jobs, schedules, observability |
| Ingestion | dlt | MongoDB extraction and Snowflake loading |
| Warehouse | Snowflake | Central analytical storage |
| Transform | dbt | Staging, intermediate, marts modeling |
| Data Quality | Soda | Runtime checks and policy enforcement |
| Contracts | YAML + Python guards | MART schema/version governance |
| Analytics | pandas + scikit-learn | Ad-hoc BI/ML end-user outputs |
| Python Tooling | uv | Dependency and command execution |

## 📁 Project Structure

```text
dagster-mflix/
├── dagster_mflix/
│   ├── assets/                    # mongodb, dbt, quality, end_user assets
│   ├── jobs/                      # movies, transform, quality, ad_hoc, bi, ml jobs
│   ├── resources/                 # dlt, dbt, snowflake resources
│   ├── partitions/
│   └── schedules/
├── mflix_snowflake/               # dbt project (staging/intermediate/marts)
├── soda/                          # soda checks and datasource config
├── data/                          # local output datasets for end users
├── data_contracts/                # mart contracts + release notes
├── images/                        # exported diagrams and screenshots
├── excalidraw/                    # editable diagram sources
├── dagster_mflix_tests/           # tests
├── docs/                          # implementation/project docs
└── _bmad-output/                  # planning and implementation artifacts
```

## 🚀 Getting Started

### 1. Requirements

- Python 3.11+
- uv
- Snowflake credentials
- MongoDB access (or sample source setup)

### 2. Setup

```bash
git clone <your-repo-url>
cd dagster-mflix
uv sync
```

### 3. Environment Variables

Set at least:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`

## ⚙️ Run the Platform

### Start Dagster

```bash
uv run dagster dev -m dagster_mflix
```

### Build dbt Models

```bash
cd mflix_snowflake
uv run dbt parse
uv run dbt build
```

### Run New End-user dbt Dashboard Models Only

```bash
cd mflix_snowflake
uv run dbt build --select dashboard_top_movies_monthly dashboard_engagement_daily dashboard_genre_trend_daily dashboard_rating_distribution
```

## 🧪 Validation

```bash
uv run pytest -q
uv run pytest -q dagster_mflix_tests/test_data_contracts.py
```

## 📚 Documentation

- `docs/dashboard-consumption.md`
- `data_contracts/mart_contracts.yml`
- `data_contracts/mart_contracts_release_notes.md`
- `excalidraw/README.md`

## 🤝 Presentation Note

This repository is now structured in the same presentation direction as the two references:

- portfolio-style README sections
- dedicated `images/` and `excalidraw/` folders
- explicit outputs and screenshots section

If you provide real screenshots, this README can look fully production-grade for end-user demos.
