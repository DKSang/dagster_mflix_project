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

## 📸 Pipeline Execution

To see the pipeline in action:

1. Start Dagster UI and navigate to the assets view to see the full DAG.
2. Trigger a job run and monitor the execution.
3. Check `logs/quality_audit/` for quality gate results.
4. Export CSV outputs from `data/` for downstream consumption.

For production screenshots, run Dagster locally and capture from the UI.

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

Example .env:

```bash
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=user_name
SNOWFLAKE_PASSWORD=your_secret_password
```

> ⚠️ Never commit `.env` to version control. Use `.gitignore` to exclude it.

## ⚙️ Run the Platform

### Start Dagster

```bash
uv run dagster dev -m dagster_mflix
```

Then open http://localhost:3000 in your browser.

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

### Run End-user Jobs Directly (Without Orchestration)

```bash
# Ad-hoc genre report
uv run python -c "from dagster_mflix.assets.end_user import ad_hoc_genre_interest_report; ad_hoc_genre_interest_report()"

# BI KPI snapshot
uv run python -c "from dagster_mflix.assets.end_user import bi_kpi_snapshot; bi_kpi_snapshot()"

# ML monthly forecast
uv run python -c "from dagster_mflix.assets.end_user import ml_monthly_rating_forecast; ml_monthly_rating_forecast()"
```

Outputs will be written to `data/` folder.

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

This repository is structured as a production-grade data engineering project:

- **Portfolio-ready README** with clear architecture, features, and quick-start sections.
- **Dedicated `images/` and `excalidraw/`** folders for diagrams and visual documentation.
- **Three end-user jobs** (ad-hoc, BI, ML) demonstrating real downstream consumption patterns.
- **Quality-first design** with Soda checks and audit logs at each pipeline stage.
- **Contract governance** for MART schemas with semantic versioning.

Perfect for demonstrating modern data stack knowledge in interviews or client presentations.

## 📖 Contributing & License

This project is open for contributions and improvements. Please follow the existing code patterns and run tests before submitting.

Licensed under MIT — see LICENSE for details.
