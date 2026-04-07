# Story 5.1: Publish and Version MART Data Contracts

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Downstream Consumer,
I want versioned data contracts for MART datasets,
so that I can integrate dashboards and services against stable schemas.

## Acceptance Criteria

1. Given MART models are available, when contract definitions are published, then each critical mart exposes schema, grain, and key semantics in versioned contract artifacts.
2. Given MART models are available, when contract definitions are published, then breaking contract changes require explicit version increment and release notes.

## Tasks / Subtasks

- [x] Xac dinh pham vi critical MART datasets cho contract versioning (AC: 1)
  - [x] Lap danh sach toi thieu cac model mart critical dang phuc vu downstream consumption (dim/fct/agg).
  - [x] Chot bo truong contract bat buoc: schema, grain, key semantics, owner, SLA/freshness, va status.
- [x] Thiet ke va tao contract artifacts co version (AC: 1, 2)
  - [x] Chon vi tri contract theo architecture baseline: data_contracts/.
  - [x] Tao mart contract file voi version metadata ro rang, co quy tac naming nhat quan.
  - [x] Dam bao moi dataset critical co section schema/grain/key semantics day du.
- [x] Chot quy trinh breaking-change va release notes (AC: 2)
  - [x] Dinh nghia tieu chi breaking change cho contract schema va semantics.
  - [x] Bat buoc bump version khi co breaking change.
  - [x] Ghi release notes tom tat thay doi va tac dong downstream.
- [x] Dong bo contract voi dbt model/testing metadata (AC: 1, 2)
  - [x] Doi chieu contract voi dbt model names va columns hien co trong MART.
  - [x] Bao dam contract va dbt schema tests khong mau thuan.
- [x] Bo sung guardrail tests/validation cho contract artifacts (AC: 1, 2)
  - [x] Them test/validation nhe de phat hien thieu field contract bat buoc.
  - [x] Them check policy de chan thay doi breaking ma khong bump version.

## Dev Notes

Story nay mo Epic 5 va tao nen tang contract-first cho downstream enablement. Muc tieu la chot artifact contracts cho MART de dashboard/API consumers tich hop on dinh ma khong can doc lai logic transform noi bo.

### Technical Requirements

- FR scope truc tiep: FR54.
- FR lien quan can giu compatibility: FR53, FR55, FR57.
- NFR lien quan: NFR3, NFR8, NFR11, NFR13, NFR15, NFR16, NFR17.
- Governance policy bat buoc: versioned changes cho model/check rules va audit/reproducibility context.

### Architecture Compliance

- Tuan thu boundary hien tai: contracts tach rieng khoi orchestration va transform code.
- Khong chen business transform vao Dagster orchestration layer khi lam story nay.
- Naming conventions:
  - Schema names: UPPER_SNAKE_CASE (neu tham chieu zone boundary).
  - Model/table/column keys: lower_snake_case.
- Pattern enforcement:
  - Moi thay doi contract co traceability ve FR/NFR.
  - Khong thay doi semantics dataset ma khong ghi ro release note.

### Library / Framework Requirements

- Story nay uu tien artifact/document contract va validation nhe, khong yeu cau nang cap framework.
- Stack runtime tham chieu theo architecture baseline hien co:
  - Dagster 1.7.7 dang duoc su dung trong repo.
  - dbt-core/dbt-snowflake theo 1.8.x range trong project.
- Neu can script validate contract, uu tien Python tooling da co trong repo va chay bang uv.

### File Structure Requirements

Uu tien can thiep toi thieu, dung dung boundary:

- Tao moi thu muc/file contract neu chua ton tai:
  - `data_contracts/mart_contracts.yml`
- Co the bo sung tai lieu huong dan contract/release notes:
  - `docs/` (chi khi can thiet cho governance clarity)
- Co the bo sung test/validation:
  - `dagster_mflix_tests/` hoac script check nhe phu hop CI flow hien co.

Khong lam trong story nay:

- Khong doi logic dbt SQL cua marts neu khong co gap contract mismatch bat buoc.
- Khong mo rong onboarding entity moi (thuoc Story 5.3).
- Khong trien khai BI/API integration runtime (thuoc Story 5.4).

### Testing Requirements

- Validate contract artifact day du cac field bat buoc: dataset, version, schema, grain, keys, owner, change_type.
- Validate policy bump version cho breaking changes.
- Chay test bang uv-first:
  - `uv run pytest -q`
  - Neu co test rieng cho contract: `uv run pytest dagster_mflix_tests -q`

### Previous Story Intelligence

- Khong ap dung. Day la story dau tien cua Epic 5.

### Git Intelligence Summary

- Epic 5 dang o trang thai backlog; chua co story implementation truoc do trong epic nay.
- Pattern tu cac story truoc: artifact format can day du guardrails, task breakdown ro, va references truy vet duoc.

### Latest Tech Information

- Khong co yeu cau buoc phai cap nhat library versions trong scope story 5.1.
- Trong truong hop bo sung contract validation tooling, uu tien giai phap tuong thich voi dependency lock hien tai.

### Project Structure Notes

- Architecture planning co de xuat `data_contracts/` nhung workspace hien tai chua co thu muc nay.
- Story 5.1 co the tao `data_contracts/` nhu mot bo phan natural cua downstream contract boundary, khong can refactor cac module khac.
- Can giu alignment voi policy quality-first: contract thay doi phai tuong thich luong dbt test/quality gate.

### References

- `_bmad-output/planning-artifacts/epics.md` (Epic 5 + Story 5.1 + Acceptance Criteria)
- `_bmad-output/planning-artifacts/prd.md` (Journey 5, FR53-FR57, NFR3/NFR13/NFR15/NFR16)
- `_bmad-output/planning-artifacts/architecture.md` (Data contracts, structure patterns, enforcement guidelines)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (story lifecycle status)
- `pyproject.toml` (dependency/runtime boundaries)

## Dev Agent Record

### Agent Model Used

GPT-5.3-Codex

### Debug Log References

- /home/dksan/.vscode-server/data/User/workspaceStorage/9eaa804812db6b9dd8495ea4072deb70/GitHub.copilot-chat/debug-logs/c486bce9-8da9-4d9e-b1dc-424289c33629
- /home/dksan/.vscode-server/data/User/workspaceStorage/9eaa804812db6b9dd8495ea4072deb70/GitHub.copilot-chat/debug-logs/c486bce9-8da9-4d9e-b1dc-424289c33629

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Story 5.1 context consolidated from Epic/PRD/Architecture with contract-first guardrails.
- Implementation constraints and out-of-scope boundaries documented to avoid regressions.
- Implemented versioned MART contract artifact in data_contracts with schema/grain/key semantics for critical dim/fct/agg datasets.
- Implemented breaking-change detection and semantic version policy enforcement utilities.
- Added release notes with explicit breaking-change rules and downstream migration expectation.
- Added automated tests for contract required fields, dbt schema alignment, and version bump policy.
- Validation completed: uv run pytest -q dagster_mflix_tests/test_data_contracts.py and uv run pytest -q.

### File List

- _bmad-output/implementation-artifacts/5-1-publish-and-version-mart-data-contracts.md
- _bmad-output/implementation-artifacts/sprint-status.yaml
- dagster_mflix/contracts.py
- data_contracts/mart_contracts.yml
- data_contracts/mart_contracts_release_notes.md
- dagster_mflix_tests/test_data_contracts.py

## Change Log

- 2026-04-07: Implemented Story 5.1 contract artifacts, breaking-change policy, and automated validations; story moved to review.