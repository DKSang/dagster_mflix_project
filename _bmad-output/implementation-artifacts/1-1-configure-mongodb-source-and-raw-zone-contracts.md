# Story 1.1: Configure MongoDB Source and RAW Zone Contracts

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Data Engineer,
I want to configure MongoDB source connections and RAW schema targets,
so that ingestion jobs can run against consistent source and destination contracts.

## Acceptance Criteria

1. Given MongoDB credentials and Snowflake targets are provided, when source configuration is validated in pipeline resources, then connection checks pass for approved collections comments and embedded_movies.
2. Given MongoDB credentials and Snowflake targets are provided, when source configuration is validated in pipeline resources, then RAW destination schemas and naming conventions are verified as MFLIX_RAW-compliant.

## Tasks / Subtasks

- [ ] Chot contract ket noi MongoDB va Snowflake cho ingest layer (AC: 1, 2)
  - [ ] Xac dinh bo bien moi truong toi thieu cho MongoDB va Snowflake.
  - [ ] Bo sung validation fail-fast khi thieu credential bat buoc.
  - [ ] Bao dam secret chi doc tu env/secret manager, khong hard-code.
- [ ] Chuan hoa source resources cho comments va embedded_movies (AC: 1)
  - [ ] Tao/bo sung ham validate collection allowlist: comments, embedded_movies.
  - [ ] Bao dam connection test co thong diep loi ro rang theo error taxonomy.
- [ ] Chuan hoa RAW contract truoc khi ingest thuc thi (AC: 2)
  - [ ] Rang buoc target schema naming theo MFLIX_RAW boundary.
  - [ ] Khong dua business transform vao ingest config/resource.
  - [ ] Ghi metadata contract de story 1.2 tai su dung.
- [ ] Tang cuong observability cho buoc validation (AC: 1, 2)
  - [ ] Emit run metadata: stage, component, error_type, run_id, timestamp.
  - [ ] Bao dam trang thai ket thuc nhat quan: success/failed/partial.
- [ ] Bo sung test cho source config va RAW contract checks (AC: 1, 2)
  - [ ] Test happy path cho 2 collections hop le.
  - [ ] Test fail path khi schema target khong dung convention.
  - [ ] Test fail path khi credential thieu hoac ket noi that bai.

## Dev Notes

Story nay la story nen cua Epic 1. Muc tieu la chot contract va guardrails cho ingest, de cac story sau (1.2-1.5) khong phai sua lai boundary hay secret pattern.

### Technical Requirements

- FR scope truc tiep: FR1, FR10.
- FR lien quan can giu compatibility: FR31-FR38 (job boundaries, run state, logs/lineage/recovery).
- NFR bat buoc cho story nay: NFR5, NFR6, NFR7, NFR8, NFR9, NFR11, NFR13, NFR15, NFR17.
- Ingestion policy bat buoc: dlt chi load raw, khong chen business logic.
- Security policy bat buoc: least privilege theo zone, secret qua env/manager.

### Architecture Compliance

- Giu boundary 3 lop du lieu: MFLIX_RAW -> STAGING -> MART; story 1.1 chi dung boundary RAW.
- Tuan thu naming conventions:
  - Schema: UPPER_SNAKE_CASE (muc tieu contract: MFLIX_RAW).
  - Python module/function/variable: lower_snake_case.
- Tuan thu process patterns:
  - Retry chi cho transient errors.
  - Contract/logic errors phai fail-fast.
- Tuan thu communication format:
  - Logging metadata: stage, component, error_type, message, run_id, timestamp.

### Library / Framework Requirements

- Dagster orchestration dang theo dependency lock hien tai: dagster==1.7.7.
- dagster-embedded-elt dang duoc dung cho dlt assets.
- dlt dang duoc pin theo range rong (>=0.3.5) trong project; can tranh su dung API moi khong tuong thich voi code hien co neu chua cap nhat lock strategy.
- dbt-core/dbt-snowflake dang theo 1.8.x range trong project; story nay khong thay doi dbt models.
- Thong tin latest tham khao de quyet dinh nang cap sau (khong bat buoc cho story nay):
  - dagster 1.12.22 (PyPI, released 2026-04-02)
  - dlt 1.24.0 (PyPI, released 2026-03-19)
  - dbt-core 1.11.7 (PyPI, released 2026-03-04)

### File Structure Requirements

Uu tien su dung va mo rong file hien co (khong re-scaffold):

- `dagster_mflix/assets/mongodb.py`
  - Giu dlt source binding cho comments, embedded_movies.
  - Bo sung/gan validation call truoc khi run ingest (neu can, thong qua helper/resource).
- `dagster_mflix/resources/__init__.py`
  - Chuan hoa env var contracts va schema contract cho Snowflake resource.
  - Khong hard-code gia tri moi nhay cam.
- `dagster_mflix/mongodb/helpers.py`
  - Dat cac helper validation source/collection/retry classification.
- `dagster_mflix_tests/`
  - Them test moi cho config validation va RAW contract checks.

Khong lam trong story nay:

- Khong tao transform logic dbt.
- Khong sua story-level behavior cua quality_job.
- Khong doi ingestion sang local file/pandas flow.

### Testing Requirements

- Python tests (pytest) bat buoc cho:
  - Validation credentials va collection allowlist.
  - Validation RAW schema contract va naming convention.
  - Error classification cho transient vs contract/logic.
- Test outputs phai de debug duoc (assert message co context).
- Khong pass story neu chi co manual test.

### Previous Story Intelligence

- Khong ap dung. Day la story dau tien cua Epic 1.

### Git Intelligence Summary

- Khong co previous story commit context can phu thuoc cho story 1.1.
- Pattern hien tai can giu: tan dung file/module hien co thay vi tao khung moi.

### Latest Tech Information

- Latest stable release tham khao tu PyPI:
  - dagster 1.12.22
  - dlt 1.24.0
  - dbt-core 1.11.7
- Huong dan cho dev:
  - Trien khai theo dependency hien tai cua repo truoc.
  - Neu can API moi, ghi ro migration note va compatibility impact trong PR.

### Project Structure Notes

- Architecture doc de xuat split resources thanh nhieu file rieng, nhung codebase hien dang de trong `dagster_mflix/resources/__init__.py`.
- Story 1.1 duoc phep incremental refactor, khong bat buoc tach module lon ngay neu gay rui ro regression.
- dbt schema hien dang la `mflix` (lowercase) trong project config; story nay uu tien contract validation layer ingest, chua ep buoc migration schema ngay lap tuc.

### References

- `_bmad-output/planning-artifacts/epics.md` (Epic 1 + Story 1.1 + AC)
- `_bmad-output/planning-artifacts/prd.md` (FR1, FR10, FR31-38, NFR5-11, NFR13-17)
- `_bmad-output/planning-artifacts/architecture.md` (Core Architectural Decisions, Implementation Patterns, Project Structure & Boundaries)
- `dagster_mflix/assets/mongodb.py` (hien trang dlt source + asset wiring)
- `dagster_mflix/resources/__init__.py` (hien trang resource contracts)
- `dagster_mflix/mongodb/helpers.py` (helper extension point)
- `pyproject.toml` (dependency constraints)
- `https://pypi.org/project/dagster/`
- `https://pypi.org/project/dlt/`
- `https://pypi.org/project/dbt-core/`

## Dev Agent Record

### Agent Model Used

GPT-5.3-Codex

### Debug Log References

- /home/dksan/.vscode-server/data/User/workspaceStorage/9eaa804812db6b9dd8495ea4072deb70/GitHub.copilot-chat/debug-logs/674002f8-9603-44d2-995a-e7a1612f2af6

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Story foundation extracted from Epic 1 and aligned with PRD/Architecture boundaries.
- Guardrails added to prevent wrong file placement, secret leakage, and ingest/business-transform mixing.

### File List

- _bmad-output/implementation-artifacts/1-1-configure-mongodb-source-and-raw-zone-contracts.md
