# Story 1.2: Implement dlt Raw Ingestion for Core Collections

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Data Engineer,
I want to ingest comments and embedded_movies into RAW using dlt,
so that source data is available in immutable raw form for downstream transforms.

## Acceptance Criteria

1. Given source and destination contracts are configured, when ingestion is executed for comments and embedded_movies, then raw tables are created or updated in MFLIX_RAW without business transformations.
2. Given source and destination contracts are configured, when ingestion is executed for comments and embedded_movies, then ingestion metadata includes source collection identity and run correlation fields.

## Tasks / Subtasks

- [ ] Chot cau hinh dlt ingestion cho 2 collection comments va embedded_movies (AC: 1)
  - [ ] Giu dlt source hien co trong `dagster_mflix/assets/mongodb.py`, khong mo rong them collection.
  - [ ] Bao dam write_disposition va pipeline config phu hop ingestion RAW.
- [ ] Dam bao ingest khong chen business transform (AC: 1)
  - [ ] Khong them transform logic vao asset ingest.
  - [ ] Chi load du lieu raw tu source vao Snowflake zone da dinh.
- [ ] Bo sung metadata cho truy vet source va run (AC: 2)
  - [ ] Bao dam run metadata co run_id va source collection identity.
  - [ ] Ghi log ngan gon de debug ingest run.
- [ ] Bo sung test cho ingest core collections (AC: 1, 2)
  - [ ] Test flow ingest chi dung comments, embedded_movies.
  - [ ] Test metadata co run correlation thong qua log/asset event duoc expose.

## Dev Notes

Story 1.2 tiep noi Story 1.1. Muc tieu la thuc thi ingest RAW on dinh voi dlt tren codebase hien co, khong refactor lon, khong doi architecture files.

### Technical Requirements

- FR scope truc tiep: FR2, FR9, FR10.
- NFR lien quan: NFR5, NFR6, NFR7, NFR9, NFR11, NFR13.
- Policy bat buoc: dlt chi ingest raw, khong chen business transform.

### Architecture Compliance

- Boundary bat buoc: MongoDB -> RAW (khong nhay truc tiep sang STAGING/MART).
- Naming conventions:
  - Python modules/functions/variables: lower_snake_case.
  - Schema contracts theo huong UPPER_SNAKE_CASE o tai lieu kien truc; tuy nhien implementation can giu compatibility voi code va env hien tai.
- Error handling: fail ro rang, de truy vet ingestion issue nhanh.

### Library / Framework Requirements

- Tiep tuc su dung stack dang co trong project:
  - dagster==1.7.7
  - dagster-embedded-elt==0.23.7
  - dlt[snowflake]>=0.3.5
- Khong thay doi dependency neu khong can thiet cho scope story.

### File Structure Requirements

Uu tien chinh sua toi thieu tren file hien co:

- `dagster_mflix/assets/mongodb.py`
  - Day la diem chinh cho implement ingest logic story 1.2.
- `dagster_mflix/mongodb/__init__.py`
  - Chi sua neu can de bo sung metadata/truy vet va van giu behavior dlt source.
- `dagster_mflix_tests/test_assets.py`
  - Dat test nho, don gian, phu hop style code hien tai.

Khong lam trong story nay:

- Khong refactor cau truc module lon.
- Khong doi luong transform/dbt.
- Khong them quality_job logic.

### Testing Requirements

- Python tests (pytest) cho:
  - ingest scope chi co comments va embedded_movies.
  - metadata truy vet source/run duoc expose theo behavior da xac dinh.
- Chay test bang uv:
  - `uv run pytest dagster_mflix_tests/test_assets.py -q`
  - `uv run pytest -q`

### Previous Story Intelligence

- Story 1.1 da tao context va contract guidance; trong thuc te implementation hien tai dang uu tien don gian theo code co san.
- Dev preference tu user: tranh over-engineering, tranh refactor phuc tap, bam sat file hien co.

### Git Intelligence Summary

- Chua co previous implementation commit cho 1.1 trong sprint nay.
- Can giu thay doi nho, dung scope 1.2.

### Latest Tech Information

- Khong bat buoc nang cap phien ban trong story nay.
- Neu gap deprecation warning trong dlt, ghi note va defer cho story ky thuat rieng.

### Project Structure Notes

- Code ingest hien dang nam o `dagster_mflix/assets/mongodb.py` va source helper o `dagster_mflix/mongodb/`.
- Story 1.2 nen uu tien wiring behavior va metadata tracking thay vi doi folder structure.

### References

- `_bmad-output/planning-artifacts/epics.md` (Epic 1 + Story 1.2 + AC)
- `_bmad-output/planning-artifacts/prd.md` (FR2, FR9, FR10 va NFR lien quan)
- `_bmad-output/planning-artifacts/architecture.md` (RAW boundary va ingestion policy)
- `_bmad-output/implementation-artifacts/1-1-configure-mongodb-source-and-raw-zone-contracts.md`
- `dagster_mflix/assets/mongodb.py`
- `dagster_mflix/mongodb/__init__.py`
- `dagster_mflix/resources/__init__.py`
- `dagster_mflix_tests/test_assets.py`

## Dev Agent Record

### Agent Model Used

GPT-5.3-Codex

### Debug Log References

- /home/dksan/.vscode-server/data/User/workspaceStorage/9eaa804812db6b9dd8495ea4072deb70/GitHub.copilot-chat/debug-logs/674002f8-9603-44d2-995a-e7a1612f2af6

### Completion Notes List

- Story 1.2 generated from sprint-order backlog (first available backlog item).
- Story context aligned with Epic 1 acceptance criteria and current codebase conventions.
- Guardrails emphasize minimal-change implementation per user preference.

### File List

- _bmad-output/implementation-artifacts/1-2-implement-dlt-raw-ingestion-for-core-collections.md
