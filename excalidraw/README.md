# Excalidraw Assets

This folder stores editable diagram sources for project documentation.

## Current Diagram Sources

- mflix-pipeline-architecture.excalidraw

## Export Guide

1. Open https://excalidraw.com/.
2. Import mflix-pipeline-architecture.excalidraw.
3. Draw/update the architecture blocks and arrows.
4. Export PNG to images/project_architecture.png.
5. (Optional) Export SVG to images/project_architecture.svg.

## Suggested Diagram Blocks

- MongoDB Source Collections
- dlt Ingestion
- Snowflake Raw Layer
- dbt Staging / Intermediate / Marts
- Soda Quality Gates
- Dagster Jobs (movies, transform, quality, ad-hoc, bi, ml)
- End-user Outputs in data/
