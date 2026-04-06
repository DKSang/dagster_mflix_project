---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
workflowType: 'epics-and-stories'
status: 'complete'
completedAt: '2026-04-05'
---

# dagster-mflix - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for dagster-mflix, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Platform Owner can register and maintain data source configurations for MongoDB collections used by the platform.
FR2: Data Engineer can trigger ingestion runs for selected collections.
FR3: Data Engineer can schedule recurring ingestion runs at defined intervals.
FR4: Data Engineer can execute incremental ingestion for eligible collections.
FR5: Data Engineer can execute full refresh ingestion when required.
FR6: Data Engineer can view ingestion run status and completion outcomes.
FR7: Data Engineer can view ingestion run history for audit and troubleshooting.
FR8: Data Engineer can retry failed ingestion runs.
FR9: Data Engineer can identify which source collections contributed to each raw dataset.
FR10: Platform can persist raw data in a dedicated raw data zone without applying business transformations.
FR11: Analytics Engineer can define and maintain standardized staging datasets for ingested sources.
FR12: Analytics Engineer can define and maintain mart datasets for analytical consumption.
FR13: Analytics Engineer can represent nested source structures as analysis-ready datasets.
FR14: Analytics Engineer can maintain conformed dimensions for movies and genres.
FR15: Analytics Engineer can maintain fact datasets for movie engagement analysis.
FR16: Analytics Engineer can maintain fact datasets for movie quality analysis.
FR17: Analytics Engineer can maintain aggregate datasets for top movies by month.
FR18: Analytics Engineer can maintain aggregate datasets for top movies by engagement.
FR19: Analytics Engineer can trace mart-level metrics back to staging and raw source lineage.
FR20: Platform can publish transformation outcomes for downstream analytical use.
FR21: Data Engineer can define mandatory data quality rules for critical fields.
FR22: Analytics Engineer can define model-level validation checks for analytical datasets.
FR23: Platform can execute quality validation as a distinct operational stage.
FR24: Platform can block or flag downstream publication when critical quality checks fail.
FR25: Platform can validate required identifiers are present in critical datasets.
FR26: Platform can validate rating values remain within accepted ranges.
FR27: Platform can validate release year/date values remain within accepted ranges.
FR28: Platform can monitor freshness of newly ingested and transformed data.
FR29: Platform can monitor daily volume changes and flag anomalous drops.
FR30: Data Engineer can review quality scan outcomes and failure details.
FR31: Platform Owner can operate ingestion, transformation, and quality workflows as distinct jobs.
FR32: Platform Owner can configure execution order dependencies across workflow stages.
FR33: Platform Owner can define run schedules for operational workflows.
FR34: Platform Owner can monitor run-level execution state across all workflow stages.
FR35: Platform Owner can access centralized logs and metadata for each run.
FR36: Platform Owner can distinguish successful, failed, and partial run outcomes.
FR37: Platform Owner can manage operational recovery actions after failures.
FR38: Platform can expose end-to-end lineage across ingestion, transformation, and quality stages.
FR39: Platform Owner can assign role-based access levels for operational and analytical users.
FR40: Platform can enforce least-privilege access boundaries across raw, staging, and mart data zones.
FR41: Platform can maintain version traceability for model and quality rule changes.
FR42: Platform can provide reproducibility context for published analytical outputs.
FR43: Platform can retain execution records needed for operational auditing.
FR44: Platform can record approval context for significant schema-affecting changes.
FR45: Platform can define data retention and usage policy boundaries for managed datasets.
FR46: Data Engineer can maintain unit tests for helper and transformation logic.
FR47: Data Engineer can maintain asset-level tests for pipeline components.
FR48: Analytics Engineer can maintain dataset-level assertions for analytical models.
FR49: Platform can execute tests as part of release-readiness and operational confidence workflows.
FR50: Team can verify expected output schema for critical analytical outputs.
FR51: Team can verify behavior when expected upstream or local artifacts are unavailable.
FR52: Team can verify correctness of ranking logic used in top-movie outputs.
FR53: Analytics Engineer can consume curated mart datasets for dashboard development.
FR54: Downstream Consumer can access stable analytical datasets through defined data contracts.
FR55: Downstream Consumer can use aggregate outputs without re-implementing upstream data preparation logic.
FR56: Platform can support phased onboarding of new source entities into the curated analytics layer.
FR57: Platform can support future integration with BI and API consumers without redefining core data semantics.

### NonFunctional Requirements

NFR1: Lich chay daily cua pipeline phai hoan tat trong khung batch window da dinh de du lieu mart san sang truoc gio phan tich.
NFR2: Thoi gian tu khi bat dau ingest den khi hoan tat quality gate cho lan chay tieu chuan khong vuot nguong van hanh ma team da cam ket noi bo.
NFR3: Cac truy van phan tich tren bang aggregate trong yeu phai dap ung du nhanh cho nhu cau dashboard dinh ky cua team analytics.
NFR4: Chay lai tung job doc lap ingest/transform/quality khong duoc gay suy giam dang ke hieu nang cac job con lai.
NFR5: Toan bo ket noi giua MongoDB, orchestration, dbt, Soda, va Snowflake phai dung kenh truyen duoc bao ve.
NFR6: Credentials va secrets phai duoc quan ly tap trung qua co che secret management, khong hard-code trong source.
NFR7: Quyen truy cap du lieu phai ap dung nguyen tac least privilege, tach quyen doc/ghi theo RAW, STAGING, MART.
NFR8: He thong phai luu audit trail cho cac lan chay va thay doi cau hinh quan trong phuc vu truy vet.
NFR9: Pipeline phai ho tro retry co kiem soat cho cac loi tam thoi o ingest va transform.
NFR10: Khi quality checks muc critical that bai, he thong phai chan hoac gan co ro rang dau ra khong dat chuan.
NFR11: Tat ca lan chay phai co trang thai ket thuc xac dinh success/failed/partial va thong tin loi du de dieu tra.
NFR12: He thong phai dam bao tinh lap lai ket qua cho cung input va cung phien ban logic bien doi.
NFR13: Tich hop MongoDB -> dlt -> Snowflake phai duy tri contract du lieu on dinh o muc schema da cong bo cho downstream.
NFR14: dbt va Soda phai tich hop trong orchestrated flow de ket qua test/check tro thanh tin hieu quyet dinh publish.
NFR15: Metadata lineage va run artifacts phai co the truy cap tap trung cho van hanh va kiem dinh.
NFR16: Moi integration moi vao pipeline phai tuan theo cung chuan quality/test gate truoc khi dua vao lich chay chinh.
NFR17: Thiet ke pipeline phai cho phep mo rong them collection va model moi ma khong can tai kien truc toan bo he thong.
NFR18: He thong phai duy tri van hanh on dinh khi tang so luong bang staging/mart theo roadmap Phase 2.
NFR19: Kien truc phai ho tro nang cap dan tu single-tenant noi bo sang mo hinh tenant-ready khi can.
NFR20: Nang luc van hanh phai mo rong theo khoi luong du lieu tang dan ma van giu duoc quality gate bat buoc.

### Additional Requirements

- Brownfield preservation is mandatory: khong re-scaffold toan bo repo; implementation phai tiep tuc tren cau truc hien huu.
- Starter template decision: No full starter scaffold command; continue from existing repository structure.
- Canonical data architecture phai tach 3 lop Snowflake: MFLIX_RAW, STAGING, MART voi boundary ro.
- Orchestration topology bat buoc: ingest_job -> transform_job -> quality_job.
- Publish policy bat buoc: chi publish/materialize outputs khi quality stage pass.
- Quality gate bat buoc: dbt tests + Soda checks trong flow orchestrated.
- Ingestion policy: dlt chi load raw, khong chua business transform logic.
- Transformation policy: dbt la noi duy nhat xu ly business transformations.
- Security and access policy: service-to-service secrets qua env/secret management + least privilege theo RAW/STAGING/MART.
- Traceability policy: run audit trail, model/check version trace, reproducibility context bat buoc.
- Error handling taxonomy bat buoc: source_connectivity_error, schema_contract_error, transform_logic_error, quality_rule_violation, warehouse_execution_error.
- Retry policy direction: chi retry loi transient; loi contract/logic phai fail-fast.
- Naming convention bat buoc: schema UPPER_SNAKE_CASE; models/columns/assets/jobs/resources lower_snake_case.
- Test enforcement policy: Python tests + dbt tests + Soda scans la quality gates trong CI.
- Integration boundary policy: khong bypass layer RAW -> MART truc tiep.
- Architecture gap to resolve in stories: chot nguong dinh luong cho batch window, retry attempts/backoff, Soda alert thresholds.
- Architecture gap to resolve in stories: chot version pinning/lock strategy va runbook incident mapping.

### UX Design Requirements

Khong tim thay UX Design document trong planning artifacts. Khong co UX-DR duoc trich xuat o buoc nay.

### FR Coverage Map

FR1: Epic 1 - Register va quan ly data source configurations cho MongoDB collections.
FR2: Epic 1 - Trigger ingestion runs cho selected collections.
FR3: Epic 1 - Schedule recurring ingestion runs.
FR4: Epic 1 - Execute incremental ingestion.
FR5: Epic 1 - Execute full refresh ingestion khi can.
FR6: Epic 1 - View ingestion run status va outcomes.
FR7: Epic 1 - View ingestion run history cho audit/troubleshooting.
FR8: Epic 1 - Retry failed ingestion runs.
FR9: Epic 1 - Trace source collections cho raw datasets.
FR10: Epic 1 - Persist raw data trong dedicated RAW zone.
FR11: Epic 2 - Define va maintain standardized staging datasets.
FR12: Epic 2 - Define va maintain mart datasets.
FR13: Epic 2 - Represent nested source structures thanh analysis-ready datasets.
FR14: Epic 2 - Maintain conformed dimensions movies va genres.
FR15: Epic 2 - Maintain fact datasets cho movie engagement.
FR16: Epic 2 - Maintain fact datasets cho movie quality.
FR17: Epic 2 - Maintain aggregate datasets top movies by month.
FR18: Epic 2 - Maintain aggregate datasets top movies by engagement.
FR19: Epic 2 - Trace mart-level metrics back to staging/raw lineage.
FR20: Epic 2 - Publish transformation outcomes cho downstream analytics.
FR21: Epic 3 - Define mandatory data quality rules cho critical fields.
FR22: Epic 3 - Define model-level validation checks.
FR23: Epic 3 - Execute quality validation as distinct stage.
FR24: Epic 3 - Block/flag downstream publication khi critical checks fail.
FR25: Epic 3 - Validate required identifiers are present.
FR26: Epic 3 - Validate rating range.
FR27: Epic 3 - Validate release year/date range.
FR28: Epic 3 - Monitor freshness.
FR29: Epic 3 - Monitor daily volume anomalies.
FR30: Epic 3 - Review quality scan outcomes.
FR31: Epic 1 - Operate ingestion/transform/quality workflows as distinct jobs.
FR32: Epic 1 - Configure execution order dependencies.
FR33: Epic 1 - Define run schedules.
FR34: Epic 1 - Monitor run-level execution states.
FR35: Epic 1 - Access centralized logs/metadata per run.
FR36: Epic 1 - Distinguish success/failed/partial outcomes.
FR37: Epic 1 - Manage recovery actions after failures.
FR38: Epic 1 - Expose end-to-end lineage across stages.
FR39: Epic 3 - Assign role-based access levels.
FR40: Epic 3 - Enforce least-privilege boundaries RAW/STAGING/MART.
FR41: Epic 3 - Maintain version traceability model/check changes.
FR42: Epic 3 - Provide reproducibility context for outputs.
FR43: Epic 3 - Retain execution records for auditing.
FR44: Epic 3 - Record approval context for schema-affecting changes.
FR45: Epic 3 - Define data retention and usage policy boundaries.
FR46: Epic 4 - Maintain unit tests for helpers/transform logic.
FR47: Epic 4 - Maintain asset-level tests.
FR48: Epic 4 - Maintain dataset-level assertions.
FR49: Epic 4 - Execute tests in release-readiness workflows.
FR50: Epic 4 - Verify expected output schema.
FR51: Epic 4 - Verify behavior when upstream/local artifacts unavailable.
FR52: Epic 4 - Verify ranking logic correctness.
FR53: Epic 5 - Consume curated mart datasets for dashboards.
FR54: Epic 5 - Access stable datasets via data contracts.
FR55: Epic 5 - Use aggregate outputs without re-implementing preparation logic.
FR56: Epic 5 - Support phased onboarding of new source entities.
FR57: Epic 5 - Support future BI/API integration without redefining data semantics.

## Epic List

### Epic 1: Raw Data Ingestion and Operational Control
Data Engineer va Platform Owner co the cau hinh nguon MongoDB, chay ingest on dinh vao RAW, theo doi run status, retry su co, va truy vet nguon du lieu de tao nen tang van hanh ban dau.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR31, FR32, FR33, FR34, FR35, FR36, FR37, FR38

### Epic 2: Curated Transformation to Analytics-Ready Models
Analytics Engineer co the chuyen du lieu tu RAW sang STAGING/MART voi schema chuan, fact/dim/aggregate ro rang, va dau ra co the dung cho phan tich dashboard.
**FRs covered:** FR11, FR12, FR13, FR14, FR15, FR16, FR17, FR18, FR19, FR20

### Epic 3: Data Quality, Governance, and Trust Controls
Team co the ap quality rules, chan publish khi critical checks fail, quan tri truy cap theo least privilege, va giu audit/reproducibility de dam bao du lieu dang tin cay.
**FRs covered:** FR21, FR22, FR23, FR24, FR25, FR26, FR27, FR28, FR29, FR30, FR39, FR40, FR41, FR42, FR43, FR44, FR45

### Epic 4: Reliability Testing and Release Confidence
Data Engineer va Analytics Engineer co the duy tri test coverage cho orchestration, transform, va quality logic, dam bao moi thay doi dat release confidence truoc khi van hanh chinh thuc.
**FRs covered:** FR46, FR47, FR48, FR49, FR50, FR51, FR52

### Epic 5: Consumption Contracts and Downstream Enablement
Analytics/Downstream Consumer co the truy cap datasets on dinh theo data contracts, tai su dung outputs ma khong lam lai chuan hoa du lieu, va mo rong onboarding entities theo roadmap.
**FRs covered:** FR53, FR54, FR55, FR56, FR57

## Epic 1: Raw Data Ingestion and Operational Control

Data Engineer va Platform Owner co the cau hinh nguon MongoDB, chay ingest on dinh vao RAW, theo doi run status, retry su co, va truy vet nguon du lieu de tao nen tang van hanh ban dau.

### Story 1.1: Configure MongoDB Source and RAW Zone Contracts

As a Data Engineer,
I want to configure MongoDB source connections and RAW schema targets,
So that ingestion jobs can run against consistent source and destination contracts.

**FRs Implemented:** FR1, FR10

**Acceptance Criteria:**

**Given** MongoDB credentials and Snowflake targets are provided
**When** source configuration is validated in pipeline resources
**Then** connection checks pass for approved collections comments and embedded_movies
**And** RAW destination schemas and naming conventions are verified as MFLIX_RAW-compliant.

### Story 1.2: Implement dlt Raw Ingestion for Core Collections

As a Data Engineer,
I want to ingest comments and embedded_movies into RAW using dlt,
So that source data is available in immutable raw form for downstream transforms.

**FRs Implemented:** FR2, FR9, FR10

**Acceptance Criteria:**

**Given** source and destination contracts are configured
**When** ingestion is executed for comments and embedded_movies
**Then** raw tables are created or updated in MFLIX_RAW without business transformations
**And** ingestion metadata includes source collection identity and run correlation fields.

### Story 1.3: Implement Ingest Job Orchestration and Scheduling

As a Platform Owner,
I want a dedicated ingest_job with daily schedule,
So that raw data refresh happens predictably and operationally.

**FRs Implemented:** FR3, FR31, FR32, FR33, FR34, FR36

**Acceptance Criteria:**

**Given** ingest assets are defined
**When** ingest_job is triggered manually or by schedule
**Then** job status is emitted as success, failed, or partial with run-level metadata
**And** scheduling configuration supports environment-specific enablement.

### Story 1.4: Add Retry and Recovery Controls for Ingestion

As a Platform Owner,
I want controlled retry and recovery behavior for transient ingest failures,
So that temporary disruptions do not cause prolonged RAW data unavailability.

**FRs Implemented:** FR8, FR37

**Acceptance Criteria:**

**Given** a transient ingestion failure occurs
**When** retry policy is applied
**Then** retries are attempted within configured attempt/backoff boundaries
**And** non-transient contract or logic errors fail-fast without infinite retries.

### Story 1.5: Expose Ingestion Lineage and Run History

As a Data Engineer,
I want ingestion run history and lineage traceability,
So that I can audit data origin and troubleshoot ingestion issues quickly.

**FRs Implemented:** FR6, FR7, FR35, FR38

**Acceptance Criteria:**

**Given** multiple ingestion runs have executed
**When** run metadata is queried from orchestration logs
**Then** each RAW dataset can be traced back to source collection and run id
**And** failed runs include sufficient error context for diagnosis.

## Epic 2: Curated Transformation to Analytics-Ready Models

Analytics Engineer co the chuyen du lieu tu RAW sang STAGING/MART voi schema chuan, fact/dim/aggregate ro rang, va dau ra co the dung cho phan tich dashboard.

### Story 2.1: Build Core Staging Models from Raw Sources

As an Analytics Engineer,
I want standardized staging models for comments and embedded movies,
So that raw source variability is normalized before mart modeling.

**FRs Implemented:** FR11, FR12

**Acceptance Criteria:**

**Given** RAW tables exist for comments and embedded_movies
**When** staging models are executed
**Then** stg_comments and stg_embedded_movies produce typed, normalized fields
**And** staging naming conventions follow lower_snake_case contracts.

### Story 2.2: Implement Nested Structure Flattening Models

As an Analytics Engineer,
I want flattening models for nested genres and cast,
So that downstream mart models can use relational analysis-ready structures.

**FRs Implemented:** FR13

**Acceptance Criteria:**

**Given** nested arrays exist in source movie structures
**When** flattening models run
**Then** stg_movie_genres and stg_movie_cast produce one-row-per-entity-grain outputs
**And** null and malformed nested values are handled by documented transform rules.

### Story 2.3: Build Dimension and Fact Mart Models

As an Analytics Engineer,
I want dim and fact marts for movies, genres, engagement, and quality,
So that analytics consumers can query trusted business-level entities.

**FRs Implemented:** FR14, FR15, FR16, FR19

**Acceptance Criteria:**

**Given** staging models are materialized
**When** mart models are executed
**Then** dim_movies, dim_genres, fct_movie_engagement, and fct_movie_quality are created with documented keys
**And** mart metrics are traceable to staging lineage.

### Story 2.4: Build Analytical Aggregate Models

As an Analytics Engineer,
I want aggregate marts for top movies by month and engagement,
So that dashboard and reporting use-cases can consume optimized outputs.

**FRs Implemented:** FR17, FR18

**Acceptance Criteria:**

**Given** fact and dimension marts are available
**When** aggregate models run
**Then** agg_top_movies_by_month and agg_top_movies_by_engagement are materialized with stable schema
**And** ranking logic is deterministic for equal-score tie conditions.

### Story 2.5: Orchestrate Transform Job Execution Flow

As a Platform Owner,
I want transform_job to execute dbt run in controlled sequence,
So that transformation outcomes are operationally observable and reusable by later stages.

**FRs Implemented:** FR20, FR32, FR34

**Acceptance Criteria:**

**Given** transform_job dependencies are configured
**When** transform_job runs after ingestion success
**Then** dbt transformations execute in declared dependency order
**And** transform run artifacts are available for quality stage consumption.

## Epic 3: Data Quality, Governance, and Trust Controls

Team co the ap quality rules, chan publish khi critical checks fail, quan tri truy cap theo least privilege, va giu audit/reproducibility de dam bao du lieu dang tin cay.

### Story 3.1: Define dbt and Soda Quality Rule Baseline

As a Data Engineer,
I want baseline quality rules for critical staging and mart fields,
So that data issues are detected before outputs are trusted downstream.

**FRs Implemented:** FR21, FR22, FR25, FR26, FR27

**Acceptance Criteria:**

**Given** staging and mart models are available
**When** quality rule definitions are loaded
**Then** critical checks include not-null, range, and relationship validations
**And** rule identifiers follow established naming standards.

### Story 3.2: Implement quality_job with Publish Blocking

As a Platform Owner,
I want a dedicated quality_job enforcing pass/fail publish gates,
So that no critical-failure dataset is published as trusted output.

**FRs Implemented:** FR23, FR24, FR30

**Acceptance Criteria:**

**Given** transform artifacts are present
**When** quality_job executes dbt tests and Soda scans
**Then** critical failures mark run as failed or blocked and prevent publish continuation
**And** pass results permit downstream materialization.

### Story 3.3: Add Freshness and Volume Anomaly Controls

As a QA/Data Reliability Analyst,
I want freshness and volume anomaly checks with configurable thresholds,
So that silent data degradation is surfaced quickly.

**FRs Implemented:** FR28, FR29

**Acceptance Criteria:**

**Given** historical run metrics exist
**When** new quality runs complete
**Then** freshness lag and record-volume deviations are evaluated against defined thresholds
**And** anomaly outcomes are emitted in machine-readable run metadata.

### Story 3.4: Enforce RBAC and Secret Handling Policies

As a Platform Owner,
I want role-based access and secure secret handling applied across RAW/STAGING/MART,
So that data access follows least privilege and credentials are protected.

**FRs Implemented:** FR39, FR40

**Acceptance Criteria:**

**Given** platform roles are defined
**When** access policies are applied
**Then** read/write privileges are separated by data zone and role responsibilities
**And** credentials are loaded from approved secret channels without hard-coded values.

### Story 3.5: Implement Audit and Reproducibility Trace Controls

As a Governance Stakeholder,
I want model/check version traceability and run audit records,
So that published analytics can be reproduced and compliance evidence retained.

**FRs Implemented:** FR41, FR42, FR43, FR44, FR45

**Acceptance Criteria:**

**Given** pipeline runs and model changes occur
**When** audit capture is executed
**Then** run records include version context for transforms and quality rules
**And** schema-affecting approvals are logged with reviewer and timestamp metadata.

## Epic 4: Reliability Testing and Release Confidence

Data Engineer va Analytics Engineer co the duy tri test coverage cho orchestration, transform, va quality logic, dam bao moi thay doi dat release confidence truoc khi van hanh chinh thuc.

### Story 4.1: Implement Unit Tests for Helpers and Transform Utilities

As a Data Engineer,
I want unit tests for helper and transform utility logic,
So that core transformations remain correct through iterative changes.

**FRs Implemented:** FR46

**Acceptance Criteria:**

**Given** helper and utility modules are identified
**When** unit test suite executes
**Then** critical parsing, casting, and mapping functions are covered by deterministic assertions
**And** failing assertions provide actionable diagnostics.

### Story 4.2: Implement Asset and Job-Level Tests

As a Data Engineer,
I want tests for Dagster assets and job orchestration flow,
So that stage transitions and dependency order remain consistent.

**FRs Implemented:** FR47

**Acceptance Criteria:**

**Given** ingest, transform, and quality jobs are defined
**When** orchestration tests execute
**Then** expected asset dependencies and job wiring are verified
**And** invalid stage transitions are detected as test failures.

### Story 4.3: Implement dbt Model Assertions and Relationship Tests

As an Analytics Engineer,
I want dbt assertions and relationship tests enforced in CI,
So that model integrity regressions are detected before merge or release.

**FRs Implemented:** FR48

**Acceptance Criteria:**

**Given** staging and mart models are materialized in test environment
**When** dbt tests run
**Then** key constraints and referential integrity checks execute for designated critical models
**And** CI fails on unresolved model test violations.

### Story 4.4: Add Failure Mode Tests for Missing Artifacts and Retry Paths

As a QA/Data Reliability Analyst,
I want explicit tests for missing upstream artifacts and retry behavior,
So that reliability controls are verified under degraded conditions.

**FRs Implemented:** FR49, FR51

**Acceptance Criteria:**

**Given** simulated missing upstream artifacts or transient failures
**When** reliability tests execute
**Then** retry logic triggers only for transient cases and fail-fast applies to contract violations
**And** resulting run state is reported as success, failed, or partial consistently.

### Story 4.5: Enforce Unified CI Quality Gates

As a Platform Owner,
I want unified CI gates for Python tests, dbt tests, and Soda checks,
So that releases follow a single trust policy across code, models, and data quality.

**FRs Implemented:** FR49, FR50, FR52

**Acceptance Criteria:**

**Given** pull requests modify orchestration, transforms, or quality rules
**When** CI pipeline runs
**Then** Python, dbt, and Soda checks execute in declared order
**And** merge is blocked when any mandatory gate fails.

## Epic 5: Consumption Contracts and Downstream Enablement

Analytics/Downstream Consumer co the truy cap datasets on dinh theo data contracts, tai su dung outputs ma khong lam lai chuan hoa du lieu, va mo rong onboarding entities theo roadmap.

### Story 5.1: Publish and Version MART Data Contracts

As a Downstream Consumer,
I want versioned data contracts for MART datasets,
So that I can integrate dashboards and services against stable schemas.

**FRs Implemented:** FR54

**Acceptance Criteria:**

**Given** MART models are available
**When** contract definitions are published
**Then** each critical mart exposes schema, grain, and key semantics in versioned contract artifacts
**And** breaking contract changes require explicit version increment and release notes.

### Story 5.2: Enable Dashboard Consumption for Core Analytics Outputs

As an Analytics Engineer,
I want curated engagement and trend outputs consumable by dashboard tools,
So that reporting can be delivered without re-implementing upstream preparation logic.

**FRs Implemented:** FR53, FR55

**Acceptance Criteria:**

**Given** contract-compliant marts and aggregates exist
**When** dashboard consumers query approved datasets
**Then** top movies, engagement, genre trend, and rating distribution use-cases are supported by curated outputs
**And** query interfaces align with documented dataset semantics.

### Story 5.3: Implement New Entity Onboarding Pattern

As a Data Engineer,
I want a repeatable onboarding pattern for new source entities users/movies/theaters,
So that post-MVP expansion can occur without architectural rework.

**FRs Implemented:** FR56

**Acceptance Criteria:**

**Given** a new approved source entity is selected
**When** onboarding workflow is executed
**Then** ingestion, staging, quality, and contract updates follow documented extension pattern
**And** existing marts remain backward compatible unless explicitly versioned.

### Story 5.4: Prepare BI/API Downstream Integration Readiness

As a Platform Owner,
I want downstream integration readiness for BI and API consumers,
So that future consumers can adopt outputs with minimal integration ambiguity.

**FRs Implemented:** FR57

**Acceptance Criteria:**

**Given** curated marts and contracts are in place
**When** downstream readiness checks are performed
**Then** required access paths, schema contracts, and usage guidance are documented for BI/API consumers
**And** integration validation confirms outputs can be consumed without redefining core data semantics.
