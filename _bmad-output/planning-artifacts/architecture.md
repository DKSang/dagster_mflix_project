---
stepsCompleted:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
workflowType: 'architecture'
project_name: 'dagster-mflix'
user_name: 'Dksan'
date: '2026-04-05'
lastStep: 8
status: 'complete'
completedAt: '2026-04-05'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
He thong can cung cap day du nang luc quan ly ingest, bien doi du lieu, quality validation, van hanh orchestration, governance/audit, testing assurance, va downstream consumption contracts. Kien truc can bao dam moi capability co the trien khai doc lap theo domain boundary, nhung van trace duoc end-to-end.

**Non-Functional Requirements:**
Kien truc bi chi phoi boi batch performance windows, secure secret handling, least-privilege access theo data zones, reliability voi retry va deterministic run states, integration contracts on dinh, va scalability khi mo rong collection/model ma khong tai kien truc toan bo.

**Scale & Complexity:**
Pham vi la nen tang analytics data-platform co do phuc tap trung binh-den-cao do can can bang giua toc do phat trien va ky luat van hanh production-minded.

- Primary domain: backend data platform and analytics orchestration
- Complexity level: medium-high
- Estimated architectural components: 10-14

### Technical Constraints & Dependencies

- Bat buoc stack: Dagster, dlt, Snowflake, dbt, Soda.
- Nested MongoDB structures can duoc flatten/cast o staging voi contracts ro rang.
- Incremental ingestion can co chien luoc tranh duplicate/missing khi out-of-order records.
- Quality gate la dieu kien truoc publish; test va scan khong duoc optional.
- Giam phu thuoc local file/pandas bang migration logic sang warehouse + dbt.

### Cross-Cutting Concerns Identified

- End-to-end lineage va metadata traceability.
- Data quality governance va policy-based publish decisions.
- Role-based access control theo RAW/STAGING/MART.
- Reproducibility, audit trail, va version trace cho model/check rules.

## Starter Template Evaluation

### Primary Technology Domain

Python data platform and analytics orchestration based on project requirements analysis.

### Starter Options Considered

1. Dagster fresh scaffold uvx create-dagster@latest project <name>
Phu hop greenfield; khong phu hop vi du an da co cau truc va ma nguon brownfield.

2. dbt fresh scaffold dbt init
Phu hop tao project moi; hien repo da co mflix_snowflake hoat dong.

3. dlt init scaffold source/destination bootstrap
Phu hop tao pipeline mau moi; hien stack da co thanh phan ingest tich hop voi kien truc hien huu.

### Selected Starter: Brownfield Preservation No Full Re-Scaffold

Rationale for Selection:
- Giu nguyen cau truc brownfield de bao toan tinh lien tuc cua FR/NFR da chot.
- Tranh rui ro pha vo lineage, test contracts, va orchestration dang co.
- Tap trung vao kien truc chuan hoa va migration co kiem soat thay vi tao khung moi.

### Initialization Command

```bash
# No full starter scaffold command selected for this brownfield project.
# Continue from existing repository structure.
```

### Architectural Decisions Provided by Starter

Language and Runtime:
- Python 3.11+ workspace hien huu, tiep tuc dung lam runtime chuan.

Styling Solution:
- Not applicable backend/data-platform architecture scope.

Build Tooling:
- Giu package/tooling hien tai trong repo; chuan hoa dan qua quyet dinh kien truc va CI gates.

Testing Framework:
- Tiep tuc dung pytest + dbt tests + Soda scans theo capability contract.

Code Organization:
- Giu cau truc hien co, cung co boundaries: orchestration, ingest, transform, quality, consumption.

Development Experience:
- Uu tien incremental modernization dependency alignment, observability consistency, quality gates, khong rebootstrap.

Note: Neu can tao sandbox de thu stack moi, dung workspace phu rieng, khong ap len codebase chinh.

## Core Architectural Decisions

### Decision Priority Analysis

Critical Decisions Block Implementation:
- Chot kien truc du lieu 3 lop Snowflake: RAW -> STAGING -> MART voi boundary ro.
- Chot orchestration topology trong Dagster: ingest_job -> transform_job -> quality_job.
- Chot quality gate bat buoc truoc publish dbt tests + Soda checks.
- Chot contract cho incremental ingestion va schema evolution tu MongoDB.
- Chot mo hinh secrets/access theo least privilege cho RAW/STAGING/MART.

Important Decisions Shape Architecture:
- Chuan hoa API giao tiep noi bo giua assets/resources/jobs theo data contract.
- Chuan hoa logging/metadata lineage tap trung o run-level.
- Chot chien luoc CI/CD quality gates cho dbt + tests + Soda.
- Chot chuan tach logic pandas/local file sang warehouse-first transforms.

Deferred Decisions Post-MVP:
- Multi-tenant day du hien tenant-ready design only.
- API productization va BI federation nang cao.
- Observability nang cao beyond baseline van hanh.

### Data Architecture

- Warehouse canonical: Snowflake voi schemas tach lop MFLIX_RAW, STAGING, MART.
- Ingestion: dlt chi load raw, khong chua business rules.
- Transformation: dbt la noi duy nhat chua business transform.
- Data quality: Soda + dbt test lam release gate cho datasets.
- Incremental strategy: uu tien key-based incremental, fallback full-refresh co kiem soat cho nguon khong du ordering guarantees.
- Data contracts: schema contracts o staging, versioned model/check changes de audit.

### Authentication and Security

- Authentication execution scope: service-to-service credentials qua secrets manager/env.
- Authorization: RBAC theo vai tro Platform Owner, Data Engineer, Analytics Engineer, Viewer.
- Access control: least privilege giua zones RAW/STAGING/MART.
- Secret policy: cam hard-coded credentials trong code va repo.
- Auditability: bat buoc luu run audit trail va config change trail.

### API and Communication Patterns

- Pattern chinh: data-asset oriented orchestration thay vi public app API.
- Internal interfaces: typed config/resource contracts giua Dagster assets/jobs/resources.
- Error handling: chuan phan loai loi ingest/transform/quality de retry/isolation nhat quan.
- Publish rule: chi materialize/publish outputs khi quality stage pass.
- Communication model: event/run-state driven trong Dagster instance.

### Frontend Architecture

- Not applicable cho MVP kien truc hien tai backend/data-platform first.
- UI scope gioi han o operational observability trong Dagster UI va downstream BI consumers.

### Infrastructure and Deployment

- Runtime: giu brownfield Python 3.11+ stack hien co.
- Orchestration hosting: Dagster OSS local/dev truoc, trien khai production theo pipeline CI/CD sau khi quality gates on dinh.
- Environments: toi thieu dev/prod config tach biet secrets + Snowflake targets.
- Monitoring: centralized logs + lineage + run metrics.
- Scaling: scale theo tang collections/models ma khong re-scaffold repo.
- Version posture da verify public releases:
  - Dagster latest: 1.12.22
  - dbt-core latest: 1.11.7
  - dlt latest: 1.24.0
- Upgrade strategy: incremental upgrade plan theo compatibility windows, khong nang cap dot ngot toan stack.

### Decision Impact Analysis

Implementation Sequence:
1. Chuan hoa boundaries RAW/STAGING/MART + naming conventions.
2. Chot resource contracts Snowflake, dlt, dbt, Soda.
3. Refactor orchestration thanh 3 jobs doc lap voi dependency ro.
4. Thiet lap quality gates va failure policies.
5. Bo sung CI checks cho test/dbt/Soda.
6. Migration dan logic local sang dbt/warehouse-first.

Cross-Component Dependencies:
- Ingestion contracts anh huong truc tiep staging model stability.
- Staging conventions quyet dinh chat luong marts va downstream dashboards.
- Quality policies chi phoi publish semantics va reliability cua toan he.
- RBAC/secrets model anh huong moi layer van hanh va audit.

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

Critical conflict points identified: 12 nhom co nguy co lech chuan giua cac agent naming, schema contracts, asset boundaries, error semantics, publish gates, test placement, logging, config, retries, schedule semantics, secrets, CI checks.

### Naming Patterns

Database naming conventions:
- Schema names: UPPER_SNAKE_CASE MFLIX_RAW, STAGING, MART.
- Table/model names: lower_snake_case stg_embedded_movies, fct_movie_engagement.
- Column names: lower_snake_case movie_id, released_year.
- Keys:
  - Primary key: <entity>_id
  - Foreign key: <referenced_entity>_id
- Test/check IDs: lower_snake_case, prefixed theo loai not_null_movie_id, range_rating_valid.

API/contract naming conventions:
- Asset keys, job names, schedule names: lower_snake_case ingest_job, quality_job_daily.
- Resource keys: lower_snake_case snowflake_resource, dbt_cli_resource.
- Run tags/metadata keys: lower_snake_case.

Code naming conventions:
- Python files/modules/functions/variables: lower_snake_case.
- Python classes/types: PascalCase.
- Constants/env keys: UPPER_SNAKE_CASE.
- dbt model filenames: lower_snake_case, prefix theo layer stg_, dim_, fct_, agg_.

### Structure Patterns

Project organization:
- Dagster orchestration code trong dagster_mflix/ theo domains:
  - assets/ cho asset definitions
  - jobs/ cho job wiring
  - resources/ cho external integrations
  - schedules/ cho runtime cadence
- dbt project giu tach biet trong mflix_snowflake/.
- Tests:
  - Python tests trong dagster_mflix_tests/
  - dbt tests trong dbt project schema.yml + singular tests
  - Soda checks trong thu muc checks rieng theo layer.

File structure patterns:
- Khong dat business transform logic vao ingestion module.
- Khong dat warehouse SQL logic vao Dagster assets tru orchestration wrappers.
- Moi file xu ly mot concern chinh; tranh file da muc dich.

### Format Patterns

API response and execution formats:
- Internal execution outcome chuan hoa theo status vocabulary:
  - success, failed, partial.
- Error payload/log fields toi thieu:
  - stage, component, error_type, message, run_id, timestamp.

Data exchange formats:
- Date/time chuan ISO 8601 UTC khi luu metadata trao doi.
- Null semantics:
  - Dung SQL NULL thuc; khong thay bang sentinel values tuy tien.
- Boolean semantics:
  - Dung true/false nhat quan qua Python/dbt/Soda configs.
- JSON/config keys: lower_snake_case.

### Communication Patterns

Event and run-state patterns:
- Stage transitions bat bien:
  - ingest completed -> transform start
  - transform completed -> quality start
  - quality passed -> publish/materialize
- Khong cho phep skip quality gate trong scheduled production path.
- Retry events phai giu correlation qua run_id/attempt_number.

State management patterns:
- Job-level state la source of truth cho operational status.
- Asset-level state phuc vu lineage/detail, khong ghi de run-level outcome.
- Khong cap nhat state bang side effects khong log.

### Process Patterns

Error handling patterns:
- Phan loai loi theo nhom:
  - source_connectivity_error
  - schema_contract_error
  - transform_logic_error
  - quality_rule_violation
  - warehouse_execution_error
- Retry chi ap dung cho loi transient; loi contract/logic phai fail-fast.
- Khi quality critical fail: bat buoc block/flag publish.

Loading and execution patterns:
- Lich chay chuan daily cho MVP; moi mo rong cadence phai co ly do du lieu.
- Backfill/chay lai phai explicit, co tagging de tach khoi regular runs.
- Incremental strategy phai co documented fallback path ve controlled full refresh.

### Enforcement Guidelines

All AI agents MUST:
- Tuan thu naming conventions va layer boundaries neu tren.
- Khong bypass quality gate khi materialize/publish outputs.
- Moi thay doi schema/model/check phai di kem test/check cap nhat.
- Khong hard-code secrets hoac environment-specific values.
- Giu traceability: moi thay doi phai map duoc toi FR/NFR lien quan.

Pattern enforcement:
- PR checks bat buoc:
  - Python tests
  - dbt test
  - Soda scan hoac equivalent CI gate
- Review checklist theo 4 truc:
  - naming
  - boundary
  - quality gate
  - traceability.
- Pattern violations phai ghi ro trong review comment theo format:
  - pattern_violation:<category>:<rule_id>.

### Pattern Examples

Good examples:
- ingest_job chi ingest raw, khong transform business columns.
- stg_movie_genres flatten nested arrays; fct_movie_engagement chi tieu thu staging outputs.
- quality_job fail khi movie_id null vuot threshold; publish buoc sau bi chan.

Anti-patterns:
- Viet logic business truc tiep trong dlt ingestion script.
- Asset Dagster ghi CSV local lam source-of-truth cho marts.
- Dat model dbt ten camelCase hoac thieu prefix layer.
- Cho phep publish du Soda/dbt critical checks fail.

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
dagster-mflix/
├── pyproject.toml
├── README.md
├── setup.cfg
├── setup.py
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── quality-gates.yml
├── dagster_mflix/
│   ├── __init__.py
│   ├── definitions.py
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   ├── dbt_transform.py
│   │   ├── quality_checks.py
│   │   └── marts_publish.py
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── ingest_job.py
│   │   ├── transform_job.py
│   │   └── quality_job.py
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── snowflake_resource.py
│   │   ├── dlt_resource.py
│   │   ├── dbt_resource.py
│   │   └── soda_resource.py
│   ├── schedules/
│   │   ├── __init__.py
│   │   ├── daily_schedule.py
│   │   └── backfill_schedule.py
│   ├── partitions/
│   │   └── __init__.py
│   └── mongodb/
│       ├── __init__.py
│       ├── helpers.py
│       └── README.md
├── dagster_mflix_tests/
│   ├── __init__.py
│   ├── test_assets.py
│   ├── test_jobs.py
│   ├── test_resources.py
│   └── test_transform_contracts.py
├── mflix_snowflake/
│   ├── dbt_project.yml
│   ├── packages.yml
│   ├── macros/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_comments.sql
│   │   │   ├── stg_embedded_movies.sql
│   │   │   ├── stg_movie_genres.sql
│   │   │   └── stg_movie_cast.sql
│   │   ├── marts/
│   │   │   ├── dim_movies.sql
│   │   │   ├── dim_genres.sql
│   │   │   ├── fct_movie_engagement.sql
│   │   │   ├── fct_movie_quality.sql
│   │   │   ├── agg_top_movies_by_month.sql
│   │   │   └── agg_top_movies_by_engagement.sql
│   │   └── schema.yml
│   ├── tests/
│   │   ├── relationships/
│   │   └── assertions/
│   └── snapshots/
├── soda/
│   ├── checks/
│   │   ├── staging_checks.yml
│   │   └── mart_checks.yml
│   └── config/
│       └── soda_configuration.yml
├── data_contracts/
│   ├── staging_contracts.yml
│   └── mart_contracts.yml
├── docs/
│   ├── architecture/
│   │   ├── decisions.md
│   │   ├── lineage.md
│   │   └── runbook.md
│   └── standards/
│       ├── naming.md
│       └── quality-gates.md
└── _bmad-output/
  └── planning-artifacts/
    ├── prd.md
    └── architecture.md
```

### Architectural Boundaries

API boundaries:
- Khong public API trong MVP; boundary chinh la orchestration contracts giua jobs/resources/assets.
- External boundaries: MongoDB source, Snowflake warehouse, dbt CLI/runtime, Soda scanner runtime.

Component boundaries:
- assets/ chi mo ta data assets va orchestration-facing logic.
- jobs/ chi wiring execution flow, khong chua business transform logic.
- resources/ chi chua adapter/integration setup, khong chua pipeline business rules.
- mflix_snowflake/models/ la noi duy nhat chua SQL business transformations.

Service boundaries:
- Ingest service boundary: assets/mongodb.py + resources/dlt_resource.py.
- Transform service boundary: assets/dbt_transform.py + resources/dbt_resource.py.
- Quality service boundary: assets/quality_checks.py + resources/soda_resource.py.
- Publish boundary: assets/marts_publish.py sau khi quality pass.

Data boundaries:
- RAW zone: immutable ingest outputs.
- STAGING zone: normalization/flatten/cast contracts.
- MART zone: business-ready analytical models.
- Khong bypass layer RAW -> MART truc tiep la anti-pattern.

### Requirements to Structure Mapping

Feature/FR mapping:
- Data Ingestion Management FR1-FR10: dagster_mflix/assets/mongodb.py, dagster_mflix/jobs/ingest_job.py, resources/dlt_resource.py.
- Data Modeling and Transformation FR11-FR20: mflix_snowflake/models/staging/, mflix_snowflake/models/marts/, assets/dbt_transform.py.
- Data Quality and Validation FR21-FR30: soda/checks/, mflix_snowflake/tests/, assets/quality_checks.py, jobs/quality_job.py.
- Orchestration and Ops FR31-FR38: jobs/, schedules/, definitions.py.
- Governance and Auditability FR39-FR45: data_contracts/, docs/architecture/runbook.md, logging metadata conventions.
- Testing and Reliability FR46-FR52: dagster_mflix_tests/, mflix_snowflake/tests/, CI workflows.
- Downstream Enablement FR53-FR57: MART models + contracts + publish asset.

Cross-cutting concerns mapping:
- RBAC/secrets: resources/*, env config, deployment settings.
- Lineage/observability: Dagster definitions + docs lineage.
- Quality gates: jobs/quality_job.py + Soda/dbt tests + CI gate workflows.
- Schema contracts: data_contracts/* + dbt schema tests.

### Integration Points

Internal communication:
- Asset dependency graph trong Dagster lam source of truth cho execution order.
- Jobs dieu phoi execution stage transitions.
- Resources inject credentials/config cho tung stage.

External integrations:
- MongoDB connection qua resource rieng.
- Snowflake qua connector/dagster-snowflake/dbt target.
- dbt runner cho transform/test.
- Soda runner cho quality scan.
- Optional BI consumers doc MART schemas theo contracts.

Data flow:
- MongoDB collections -> dlt ingest -> Snowflake RAW.
- dbt run: RAW -> STAGING -> MART.
- dbt test + Soda scan: validate STAGING/MART.
- Neu pass: publish/materialize outputs; neu fail: block/flag outputs.

### File Organization Patterns

Configuration files:
- Root: runtime/build/project config.
- dbt config trong mflix_snowflake/.
- Soda config tach trong soda/config/.
- Contracts tach rieng trong data_contracts/.

Source organization:
- Python orchestration code theo domain modules.
- SQL transformations tach rieng theo layer va subject.

Test organization:
- Python tests cho orchestration/resources/helpers.
- dbt tests cho model-level guarantees.
- Soda checks cho runtime quality gates.

Asset organization:
- Khong dung local CSV lam source-of-truth cho analytical marts.
- Local data/ chi phuc vu sample hoac temporary artifacts, khong la production boundary.

### Development Workflow Integration

Development server structure:
- Dagster dev server dung definitions.py lam entrypoint.
- dbt local workflow chay trong mflix_snowflake/.
- Quality checks chay doc lap hoac trong orchestrated job.

Build process structure:
- CI chay theo thu tu: lint/tests -> dbt test -> soda checks -> integration validation.
- Moi gate fail se chan merge/deploy.

Deployment structure:
- Deploy theo environment tach biet secrets + Snowflake targets.
- Runtime jobs/schedules bat theo environment policy.
- Audit/log artifacts duoc luu tap trung phuc vu dieu tra su co.

## Architecture Validation Results

### Coherence Validation

Decision Compatibility:
- Stack Dagster + dlt + Snowflake + dbt + Soda tuong thich voi muc tieu warehouse-first va orchestration-first.
- Quyet dinh brownfield preservation nhat quan voi pham vi MVP va tranh re-scaffold risk.
- Layer boundaries RAW/STAGING/MART nhat quan voi quality gate va publish semantics.

Pattern Consistency:
- Naming, structure, format, communication, process patterns da du de tranh xung dot agent-level.
- Error taxonomy va quality-pass-before-publish rule phu hop voi reliability NFRs.
- RBAC, audit trail, reproducibility duoc phan anh xuyen suot decisions va patterns.

Structure Alignment:
- Cau truc thu muc de xuat khop voi boundaries da chot.
- Mapping FR categories -> modules/directories ro rang.
- Integration points noi bo va external dependencies da duoc dinh tuyen theo layer.

### Requirements Coverage Validation

Functional Requirements Coverage:
- Data ingestion, transform, quality, orchestration, governance, testing, downstream enablement deu co architectural support.
- Khong thay nhom FR nao bi thieu vi tri trien khai cap module.

Non-Functional Requirements Coverage:
- Performance: duoc phan anh qua batch window mindset va quality gate orchestration.
- Security: co secrets policy, least privilege, auditability.
- Reliability: co retry/fail-fast/publish blocking semantics.
- Integration va Scalability: co contracts, boundaries, and expansion-ready structure.

### Implementation Readiness Validation

Decision Completeness:
- Major decisions da co rationale va impact sequence.
- Versions cua cong nghe chinh da duoc verify tu nguon hien tai.
- Defer list cho post-MVP da tach ro, tranh scope creep.

Structure Completeness:
- Project tree da day du o muc implementation guide.
- Boundaries va integration points da dinh nghia du ro cho phan ra stories.

Pattern Completeness:
- Conflict points chinh giua nhieu AI agents da duoc bao phu.
- Co anti-patterns cu the de tranh implementation drift.

### Gap Analysis Results

Critical gaps:
- Khong co blocker kien truc o muc khong the trien khai.

Important gaps:
- Chua chot nguong dinh luong cu the cho mot so NFR van hanh:
  - batch window target cu the,
  - retry policy gioi han attempts/backoff,
  - threshold/alert policy cho Soda volume/freshness anomalies.
- Chua chi dinh ro chuan version pinning policy giua pyproject va lock strategy.

Nice-to-have gaps:
- Chua co runbook chuan cho incident classes mapping voi error taxonomy.
- Chua co template chuan cho pattern_violation:<category>:<rule_id> trong PR checklist artifact.

### Validation Issues Addressed

- Da xac nhan khong can kien truc frontend cho MVP backend/data-platform.
- Da xac nhan huong brownfield la quyet dinh chuan cho repo hien tai.
- Da xac nhan quality gate la bat buoc truoc publish.

### Architecture Completeness Checklist

Requirements Analysis:
- [x] Project context analyzed
- [x] Complexity assessed
- [x] Constraints identified
- [x] Cross-cutting concerns mapped

Architectural Decisions:
- [x] Core decisions documented
- [x] Stack and versions verified
- [x] Integration patterns defined
- [x] Reliability/security constraints addressed

Implementation Patterns:
- [x] Naming patterns defined
- [x] Structure/format patterns defined
- [x] Communication/process patterns defined
- [x] Enforcement guidelines defined

Project Structure:
- [x] Complete structure proposed
- [x] Boundaries defined
- [x] Mapping to FR categories provided
- [x] Internal/external integration points mapped

### Architecture Readiness Assessment

Overall Status: READY FOR IMPLEMENTATION with minor clarifications
Confidence Level: High

Key strengths:
- Boundary clarity cao, de phan ra thanh epics/stories.
- Quality-first architecture giam risk du lieu sai downstream.
- Brownfield-compatible, it gian doan codebase hien huu.

Areas for future enhancement:
- Quantify operational SLO/SLA specifics.
- Chuan hoa incident runbook + PR enforcement templates.
- Formalize dependency upgrade cadence.

### Implementation Handoff

AI Agent Guidelines:
- Tuan thu tuyet doi layer boundaries va naming conventions.
- Khong bypass quality gate truoc publish.
- Moi thay doi schema/model/check phai cap nhat test/check tuong ung.
- Trace moi thay doi ve FR/NFR trong PR notes.

First implementation priority:
- Chuan hoa ingest_job, transform_job, quality_job va resource contracts trong codebase hien tai truoc khi mo rong feature set.
- Operational resilience: retry, failure isolation, rerun safety, centralized run observability.