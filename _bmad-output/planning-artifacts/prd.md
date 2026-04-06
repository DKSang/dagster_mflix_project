---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
inputDocuments:
  - README.md
  - dagster_mflix/mongodb/README.md
  - mflix_snowflake/README.md
documentCounts:
  briefCount: 0
  researchCount: 0
  brainstormingCount: 0
  projectDocsCount: 3
classification:
  projectType: saas_b2b
  domain: scientific
  complexity: medium
  projectContext: brownfield
workflowType: 'prd'
---

# Product Requirements Document - dagster-mflix

**Author:** Dksan
**Date:** 2026-04-05

## Executive Summary

Movie Analytics Platform la nen tang phan tich du lieu phim theo kien truc warehouse-first, su dung MongoDB lam nguon du lieu hoat dong va Snowflake lam trung tam luu tru, mo hinh hoa, va khai thac phan tich. San pham tap trung giai quyet khoang trong pho bien cua cac pipeline portfolio: ingest duoc du lieu nhung thieu chuan hoa lineage, quality gating, va mo hinh phan tich co the van hanh lap lai.
Nguoi dung muc tieu la data engineer, analytics engineer, va nhom phan tich can mot luong end-to-end ro rang tu raw den mart de xay dashboard, theo doi movie engagement, phat hien xu huong the loai, phan tich phan phoi rating, va giam sat chat luong du lieu theo thoi gian.
Gia tri cot loi cua san pham la bien bai toan "demo ETL" thanh mot he du lieu phan tich co cau truc van hanh thuc te: orchestration theo asset/job, kiem thu mo hinh du lieu, kiem soat chat luong dinh luong, va kha nang mo rong sang BI/API output ma khong phai tai kien truc nen tang.

### What Makes This Special

Diem khac biet khong nam o tung cong cu rieng le ma o cach ghep chung thanh mot he nhat quan theo vai tro ro rang: dlt cho raw ingestion, dbt cho chuan hoa va business modeling, Dagster cho orchestration + observability, Soda cho data quality runtime checks, va test layer de bao ve tinh dung dan qua moi lan thay doi.
Core insight cua san pham la tach roi triet de cac moi quan tam ky thuat theo tung layer du lieu (bronze/silver/gold tuong ung raw/staging/mart), tu do giam phu thuoc vao xu ly local file hoac pandas ad-hoc, tang tinh kiem soat, tai su dung, va kha nang audit.
Nguoi dung chon giai phap nay vi ho nhan duoc ca hai muc tieu cung luc: hoc sau data platform theo chuan nghe nghiep va tao ra artifact phan tich co the chung minh nang luc trien khai production-minded pipeline.

## Project Classification

Project Type: saas_b2b
Domain: scientific (data analytics/modeling)
Complexity: medium
Project Context: brownfield

## Success Criteria

### User Success

- Data engineer co the chay pipeline end-to-end MongoDB -> Snowflake -> dbt -> quality checks theo lich dinh ky ma khong can thao tac thu cong nhieu buoc.
- Analytics engineer co the truy cap cac mart/fact/dim on dinh de tao dashboard movie engagement, genre trends, rating distribution ma khong can xu ly lai du lieu raw.
- Nguoi dung noi bo co the truy vet lineage ro rang tu bang mart ve staging/raw thong qua asset graph va job dependency.
- Thoi gian tu ingest den bang phan tich san sang su dung dat muc phu hop cho phan tich dinh ky, voi trang thai chay duoc quan sat tap trung.

### Business Success

- Trong 3 thang dau, hoan thanh nen tang analytics co the demo thuc chien voi cac lop ingest/transform/quality tach bach va tai chay on dinh.
- Trong 6-12 thang, mo rong them domain entities (users, movies, theaters) ma khong pha vo kien truc chuan raw/staging/mart.
- Tang do tin cay du lieu dau ra cho dashboard thong qua quality gate, giam dang ke loi du lieu phat hien muon o lop BI.
- Tao portfolio data engineering co gia tri tuyen dung cao: the hien orchestration, modeling, data quality, testing va van hanh.

### Technical Success

- Dagster tach ro 3 job: ingest_job, transform_job, quality_job; co schedule va observability cho tung chang.
- dlt chi dam nhiem ingest raw, khong chua business logic; uu tien incremental load cho collection phu hop.
- dbt staging xu ly chuan hoa schema, flatten nested documents, cast kieu du lieu; dbt marts tao cac bang phan tich cuoi.
- Soda checks chay tai staging/mart voi cac rule cot loi: not null, valid range, freshness/volume anomaly.
- Test coverage gom unit test, asset test, dbt model test; bo sung kiem thu cho xu ly file local hien co trong giai doan chuyen doi.

### Measurable Outcomes

- 100% pipeline runs theo lich co log trang thai ro rang theo tung buoc ingest/transform/quality.
- 100% bang mart chinh co test not null cho key fields va relationships giua fact-dim.
- 100% checks bat buoc cho movie_id, title, rating range, released range duoc thuc thi moi lan chay quality_job.
- Giam phu thuoc local CSV theo lo trinh: toan bo logic phan tich trong yeu chuyen sang Snowflake + dbt models.
- Hoan thanh bo mart muc tieu ban dau: fct_movie_engagement, fct_movie_quality, dim_movies, dim_genres, agg_top_movies_by_month, agg_top_movies_by_engagement.

Cac tieu chi tren la co so de gioi han pham vi MVP va sap xep lo trinh phat trien theo tung giai doan.

## Product Scope

### MVP - Minimum Viable Product

- Ingest du lieu comments va embedded_movies tu MongoDB vao Snowflake RAW bang dlt.
- Xay dbt staging models: stg_comments, stg_embedded_movies, stg_movie_genres, stg_movie_cast.
- Xay dbt mart models cot loi cho engagement va aggregation theo thang/engagement.
- Thiet lap Dagster orchestration 3 job voi schedule toi thieu daily.
- Thiet lap Soda checks cot loi + dbt test co ban.
- Bo sung test thiet yeu cho asset/helpers/ranking logic hien co.

### Growth Features (Post-MVP)

- Mo rong ingest them users, movies, theaters khi hoan tat entity map.
- Nang quality monitoring voi alert khi freshness/volume lech nguong.
- Tang muc tu dong hoa CI cho dbt test, Soda scan, unit test.
- Chuyen hoan toan cac logic pandas/local file con lai sang dbt hoac asset doc Snowflake co kiem soat.

### Vision (Future)

- Hinh thanh nen tang movie analytics production-minded co the mo rong domain va workload.
- Cung cap dau ra on dinh cho dashboard hoac API analytics downstream.
- Tien toi data product co governance tot: lineage day du, chat luong co nguong kiem soat, va kha nang audit.

De dam bao cac muc tieu scope co the trien khai thanh nang luc cu the, cac user journey duoi day xac dinh ro cac tinh huong su dung then chot.

## User Journeys

### Journey 1 - Primary User (Success Path): Data Engineer van hanh pipeline hieu qua

Opening Scene
An, mot data engineer, dang quan ly pipeline phim nhung luong hien tai con roi roi: ingest mot noi, transform mot noi, quality check thu cong. Moi lan loi phat sinh deu ton thoi gian truy nguoc.

Rising Action
An vao Dagster, kick ingest_job tu MongoDB qua dlt len Snowflake RAW. Sau do transform_job chay dbt run de tao STAGING va MART. Cuoi cung quality_job chay dbt test + Soda scans.

Climax
Dashboard monitoring cho thay run status xanh o tat ca node, lineage map day du tu RAW -> STAGING -> MART. An confirm bang fct_movie_engagement va agg_top_movies_by_month da san sang cho team analytics.

Resolution
Tu mot quy trinh ad-hoc, An co duoc mot pipeline co the lap lai, quan sat duoc, de mo rong them collection moi ma khong pha vo kien truc.

### Journey 2 - Primary User (Edge Case): Analytics Engineer gap anomaly du lieu

Opening Scene
Binh, analytics engineer, dang tao dashboard genre trends thi thay rating distribution dot ngot lech manh so voi chu ky truoc.

Rising Action
Binh kiem tra ket qua quality run va thay Soda canh bao: rating vuot nguong hop le o mot phan ban ghi moi. Binh drill-down qua dbt test va tim ra du lieu nested flatten bi cast sai.

Climax
Binh phoi hop voi data engineer de fix model staging stg_embedded_movies, stg_movie_genres, chay lai transform + quality. Canh bao bien mat, metric tro lai on dinh.

Resolution
Binh tiep tuc phat hanh dashboard voi do tin cay cao hon. Team co duoc co che phat hien loi som truoc khi anh huong den bao cao.

### Journey 3 - Admin/Ops User: Platform Owner quan tri va lap lich chay

Opening Scene
Chi, platform owner, can dam bao he thong chay daily on dinh va co SLA noi bo cho data freshness.

Rising Action
Chi cau hinh schedule theo nhu cau (daily, co the nang len hourly cho collection quan trong), theo doi run history va alert khi job fail hoac volume/freshness lech nguong.

Climax
Mot ngay ingestion fail do ket noi MongoDB bat on dinh. Chi thay fail ngay trong orchestration view, retry co kiem soat, va job phuc hoi trong cung chu ky.

Resolution
Team van dat duoc muc tieu cap nhat du lieu dung han. Chi co bang chung van hanh (log, lineage, checks) de bao cao trang thai he thong.

### Journey 4 - Support/Troubleshooting User: QA/Data Reliability Analyst dieu tra su co

Opening Scene
Dung, QA/Data Reliability analyst, nhan bao cao rang mot bang mart co so dong giam bat thuong.

Rising Action
Dung vao ket qua Soda scan, so sanh trend volume theo ngay, doi chieu voi dbt tests va metadata ingestion. Dung khoanh vung nhanh collection gay bien dong.

Climax
Dung phat hien incremental key chua on dinh o mot collection moi, de xuat cap nhat strategy incremental va bo sung check anomaly rang buoc chat hon.

Resolution
Su co duoc xu ly co he thong, va bo check duoc nang cap de tranh lap lai. Do tin cay cua platform tang dan qua moi sprint.

### Journey 5 - API/Integration User (tuong lai): BI/Downstream Consumer su dung dau ra marts

Opening Scene
Ha, nguoi phat trien dashboard/API downstream, can nguon du lieu da chuan hoa de tich hop nhanh vao san pham phan tich.

Rising Action
Ha ket noi vao cac mart on dinh gom dim_movies, dim_genres, fct_movie_quality va cac bang aggregate, su dung convention schema nhat quan va data dictionary.

Climax
Ha phat hanh dashboard top movies by engagement theo thang ma khong can viet lai logic xu ly du lieu goc.

Resolution
Thoi gian ra mat tinh nang analytics duoc rut ngan nho su phan tach ro giua data platform va lop tieu thu.

### Journey Requirements Summary

- Can nang luc orchestration theo job tach lop: ingest, transform, quality.
- Can observability/lineage de truy vet su co tu mart ve raw.
- Can quality gates dbt + Soda voi checks not null, range, freshness, volume anomaly.
- Can strategy xu ly loi va retry cho ingestion/transform.
- Can contract schema on dinh cho downstream consumption.
- Can quy trinh cap nhat test/check khi mo rong collection moi.

## Domain-Specific Requirements

### Compliance and Governance

- Dat yeu cau reproducibility cho toan bo luong phan tich: moi metric trong mart can truy vet nguon du lieu va logic bien doi.
- Luu vet thay doi model va quality rules theo version de audit duoc ket qua theo tung lan release.
- Thiet lap data retention va access policy phu hop cho du lieu tu MongoDB sang Snowflake, tranh su dung data ngoai muc dich phan tich da dinh nghia.
- Co quy trinh phe duyet thay doi schema quan trong de tranh vo downstream dashboards.

### Technical Constraints

- Tinh nhat quan du lieu la uu tien: dbt tests + Soda checks phai chay nhu quality gate bat buoc truoc khi publish outputs.
- Nested documents tu MongoDB tao ap luc lon cho staging layer: can chuan hoa flatten/cast theo convention on dinh va co test cho tung kieu truong.
- Incremental load can duoc thiet ke can than de tranh duplicate/missing records khi co out-of-order inserts.
- Tinh san sang van hanh: ingest, transform, quality can co retry strategy, fail visibility, va run-level observability.

### Integration Requirements

- Dagster can orchestration suot tu ingest den transform va quality, dong bo metadata trang thai run cho team van hanh.
- dlt phai giu vai tro ingest raw thuan tuy, khong chen business logic vao ingestion layer.
- dbt can la noi duy nhat xu ly business transformation cho staging/mart de de audit va maintain.
- Soda can tich hop vao quality job va co co che canh bao khi freshness/volume/range vuot nguong.

### Risk Mitigations

- Rui ro drift schema tu MongoDB: giam thieu bang contracts o staging + test cho truong moi/phat sinh null bat thuong.
- Rui ro metric sai do cast/flatten: giam thieu bang data tests va regression checks tren cac model critical.
- Rui ro phu thuoc local files/pandas trong pipeline hien tai: giam thieu bang lo trinh di doi logic sang Snowflake + dbt.
- Rui ro fail muon tai lop BI: giam thieu bang chat luong du lieu duoc kiem tra som o staging va gate truoc mart publish.
- Rui ro mo rong domain entities gay no technical debt: giam thieu bang mo rong theo entity map va pattern model da chuan hoa.

## SaaS B2B Specific Requirements

### Project-Type Overview

Nen tang duoc dinh vi nhu mot analytics platform phuc vu noi bo/portfolio theo mo hinh SaaS B2B architecture patterns, nhung chua trien khai mo hinh thuong mai day du billing/tiering. Trong tam la nang luc van hanh on dinh, truy vet minh bach, va mo rong tich hop du lieu theo nhu cau doanh nghiep.

### Technical Architecture Considerations

- Ap dung ranh gioi ro giua orchestration layer Dagster, ingestion layer dlt, transformation layer dbt, quality layer Soda, va storage/compute layer Snowflake.
- Thiet ke theo pattern module hoa de de scale so luong collection, model, checks ma khong tang do ket dinh giua cac layer.
- Yeu cau metadata observability xuyen suot pipeline runs de phuc vu van hanh va audit ky thuat.

### Tenant Model

- Pha MVP van hanh theo single-tenant noi bo mot team so huu.
- Thiet ke naming conventions va schema boundaries theo huong tenant-ready de co the nang cap multi-tenant sau nay neu chuyen thanh san pham dung chung nhieu nhom.

### RBAC Matrix

- Toi thieu cac nhom quyen:
  - Platform Owner: quan tri schedule, run policies, resource config.
  - Data Engineer: chinh ingest/transform pipelines.
  - Analytics Engineer: phat trien model/dbt tests va tieu thu marts.
  - Viewer/Consumer: chi doc mart outputs va dashboard datasets.
- Quyen ghi vao RAW/STAGING/MART can tach biet theo nguyen tac least privilege.

### Integration List

- Core integrations: MongoDB source, Snowflake warehouse, dbt modeling/testing, Soda quality scans, Dagster orchestration/observability.
- Optional integrations: BI tools Metabase/Superset/Power BI, alert channels Slack/Email, CI runner cho test gates.
- Integration contracts can dinh nghia ro diem vao/ra du lieu va trach nhiem theo layer.

### Compliance Requirements

- Khong yeu cau chung chi regulatory chuyen nganh o giai doan hien tai, nhung bat buoc:
  - reproducibility cua metrics,
  - versioned changes cho models/checks,
  - audit trail cho pipeline runs,
  - kiem soat truy cap du lieu theo vai tro.

### Implementation Considerations

- Uu tien hoan thien single-tenant production-ready truoc khi can nhac multi-tenant/commercial features.
- Khong trien khai subscription tiers o MVP de tranh mo rong pham vi ngoai muc tieu pipeline.
- Dam bao moi mo rong tich hop moi di qua chuan quality gate va test gate da thiet lap.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

MVP Approach: Platform MVP huong validated learning qua kha nang van hanh end-to-end va do tin cay du lieu, thay vi feature-rich product.
Resource Requirements: 1 data engineer + 1 analytics engineer co the mot nguoi kiem nhiem de bao phu ingest, modeling, quality, test, va observability.

### MVP Feature Set (Phase 1)

Core User Journeys Supported:
- Data engineer van hanh thanh cong ingest -> transform -> quality theo lich.
- Analytics engineer tieu thu marts on dinh de tao dashboard engagement va trends.
- Ops owner theo doi run status, retry su co, va giu freshness theo muc tieu.

Must-Have Capabilities:
- dlt ingest comments va embedded_movies vao Snowflake RAW.
- dbt staging models: stg_comments, stg_embedded_movies, stg_movie_genres, stg_movie_cast.
- dbt mart models: fct_movie_engagement, fct_movie_quality, dim_movies, dim_genres, agg_top_movies_by_month, agg_top_movies_by_engagement.
- Dagster jobs tach lop: ingest_job, transform_job, quality_job + daily schedule.
- Quality gate voi dbt test + Soda checks cho not null, range, freshness/volume.
- Test nen tang: unit tests, asset tests, dbt model tests cho logic cot loi.

### Post-MVP Features

Phase 2 (Post-MVP):
- Mo rong ingest users, movies, theaters.
- Nang cap anomaly alerts va canh bao theo nguong.
- Tu dong hoa CI gates cho test + quality scans.
- Giam manh phu thuoc local CSV/pandas ad-hoc con sot lai.

Phase 3 (Expansion):
- Dong bo output voi BI/API downstream theo data contracts.
- Mo rong governance metadata catalog, policy enforcement va audit depth.
- Chuan bi kien truc tenant-ready cho kha nang san pham hoa rong hon neu can.

### Risk Mitigation Strategy

Technical Risks:
- Nested schema drift va cast sai kieu du lieu.
- Mitigation: staging contracts, test theo cot critical, regression checks tren marts.

Market Risks:
- Dashboard output chua du wow du pipeline ky thuat tot.
- Mitigation: uu tien 2-3 use cases analytics ro gia tri engagement, genre trends, rating quality de demo ket qua nhanh.

Resource Risks:
- Team nho de qua tai khi vua xay pipeline vua nang cap dashboard.
- Mitigation: gioi han scope MVP theo must-have, day growth features sang Phase 2, va standardize conventions de giam chi phi bao tri.

Tren nen pham vi da thong nhat, danh sach functional requirements duoi day la capability contract cho toan bo cac buoc thiet ke va trien khai tiep theo.

## Functional Requirements

### Data Ingestion Management

- FR1: Platform Owner can register and maintain data source configurations for MongoDB collections used by the platform.
- FR2: Data Engineer can trigger ingestion runs for selected collections.
- FR3: Data Engineer can schedule recurring ingestion runs at defined intervals.
- FR4: Data Engineer can execute incremental ingestion for eligible collections.
- FR5: Data Engineer can execute full refresh ingestion when required.
- FR6: Data Engineer can view ingestion run status and completion outcomes.
- FR7: Data Engineer can view ingestion run history for audit and troubleshooting.
- FR8: Data Engineer can retry failed ingestion runs.
- FR9: Data Engineer can identify which source collections contributed to each raw dataset.
- FR10: Platform can persist raw data in a dedicated raw data zone without applying business transformations.

### Data Modeling and Transformation

- FR11: Analytics Engineer can define and maintain standardized staging datasets for ingested sources.
- FR12: Analytics Engineer can define and maintain mart datasets for analytical consumption.
- FR13: Analytics Engineer can represent nested source structures as analysis-ready datasets.
- FR14: Analytics Engineer can maintain conformed dimensions for movies and genres.
- FR15: Analytics Engineer can maintain fact datasets for movie engagement analysis.
- FR16: Analytics Engineer can maintain fact datasets for movie quality analysis.
- FR17: Analytics Engineer can maintain aggregate datasets for top movies by month.
- FR18: Analytics Engineer can maintain aggregate datasets for top movies by engagement.
- FR19: Analytics Engineer can trace mart-level metrics back to staging and raw source lineage.
- FR20: Platform can publish transformation outcomes for downstream analytical use.

### Data Quality and Validation

- FR21: Data Engineer can define mandatory data quality rules for critical fields.
- FR22: Analytics Engineer can define model-level validation checks for analytical datasets.
- FR23: Platform can execute quality validation as a distinct operational stage.
- FR24: Platform can block or flag downstream publication when critical quality checks fail.
- FR25: Platform can validate required identifiers are present in critical datasets.
- FR26: Platform can validate rating values remain within accepted ranges.
- FR27: Platform can validate release year/date values remain within accepted ranges.
- FR28: Platform can monitor freshness of newly ingested and transformed data.
- FR29: Platform can monitor daily volume changes and flag anomalous drops.
- FR30: Data Engineer can review quality scan outcomes and failure details.

### Pipeline Orchestration and Operations

- FR31: Platform Owner can operate ingestion, transformation, and quality workflows as distinct jobs.
- FR32: Platform Owner can configure execution order dependencies across workflow stages.
- FR33: Platform Owner can define run schedules for operational workflows.
- FR34: Platform Owner can monitor run-level execution state across all workflow stages.
- FR35: Platform Owner can access centralized logs and metadata for each run.
- FR36: Platform Owner can distinguish successful, failed, and partial run outcomes.
- FR37: Platform Owner can manage operational recovery actions after failures.
- FR38: Platform can expose end-to-end lineage across ingestion, transformation, and quality stages.

### Governance, Access, and Auditability

- FR39: Platform Owner can assign role-based access levels for operational and analytical users.
- FR40: Platform can enforce least-privilege access boundaries across raw, staging, and mart data zones.
- FR41: Platform can maintain version traceability for model and quality rule changes.
- FR42: Platform can provide reproducibility context for published analytical outputs.
- FR43: Platform can retain execution records needed for operational auditing.
- FR44: Platform can record approval context for significant schema-affecting changes.
- FR45: Platform can define data retention and usage policy boundaries for managed datasets.

### Testing and Reliability Assurance

- FR46: Data Engineer can maintain unit tests for helper and transformation logic.
- FR47: Data Engineer can maintain asset-level tests for pipeline components.
- FR48: Analytics Engineer can maintain dataset-level assertions for analytical models.
- FR49: Platform can execute tests as part of release-readiness and operational confidence workflows.
- FR50: Team can verify expected output schema for critical analytical outputs.
- FR51: Team can verify behavior when expected upstream or local artifacts are unavailable.
- FR52: Team can verify correctness of ranking logic used in top-movie outputs.

### Consumption and Downstream Enablement

- FR53: Analytics Engineer can consume curated mart datasets for dashboard development.
- FR54: Downstream Consumer can access stable analytical datasets through defined data contracts.
- FR55: Downstream Consumer can use aggregate outputs without re-implementing upstream data preparation logic.
- FR56: Platform can support phased onboarding of new source entities into the curated analytics layer.
- FR57: Platform can support future integration with BI and API consumers without redefining core data semantics.

## Non-Functional Requirements

### Performance

- NFR1: Lich chay daily cua pipeline phai hoan tat trong khung batch window da dinh de du lieu mart san sang truoc gio phan tich.
- NFR2: Thoi gian tu khi bat dau ingest den khi hoan tat quality gate cho lan chay tieu chuan khong vuot nguong van hanh ma team da cam ket noi bo.
- NFR3: Cac truy van phan tich tren bang aggregate trong yeu phai dap ung du nhanh cho nhu cau dashboard dinh ky cua team analytics.
- NFR4: Chay lai tung job doc lap ingest/transform/quality khong duoc gay suy giam dang ke hieu nang cac job con lai.

### Security

- NFR5: Toan bo ket noi giua MongoDB, orchestration, dbt, Soda, va Snowflake phai dung kenh truyen duoc bao ve.
- NFR6: Credentials va secrets phai duoc quan ly tap trung qua co che secret management, khong hard-code trong source.
- NFR7: Quyen truy cap du lieu phai ap dung nguyen tac least privilege, tach quyen doc/ghi theo RAW, STAGING, MART.
- NFR8: He thong phai luu audit trail cho cac lan chay va thay doi cau hinh quan trong phuc vu truy vet.

### Reliability

- NFR9: Pipeline phai ho tro retry co kiem soat cho cac loi tam thoi o ingest va transform.
- NFR10: Khi quality checks muc critical that bai, he thong phai chan hoac gan co ro rang dau ra khong dat chuan.
- NFR11: Tat ca lan chay phai co trang thai ket thuc xac dinh success/failed/partial va thong tin loi du de dieu tra.
- NFR12: He thong phai dam bao tinh lap lai ket qua cho cung input va cung phien ban logic bien doi.

### Integration

- NFR13: Tich hop MongoDB -> dlt -> Snowflake phai duy tri contract du lieu on dinh o muc schema da cong bo cho downstream.
- NFR14: dbt va Soda phai tich hop trong orchestrated flow de ket qua test/check tro thanh tin hieu quyet dinh publish.
- NFR15: Metadata lineage va run artifacts phai co the truy cap tap trung cho van hanh va kiem dinh.
- NFR16: Moi integration moi vao pipeline phai tuan theo cung chuan quality/test gate truoc khi dua vao lich chay chinh.

### Scalability

- NFR17: Thiet ke pipeline phai cho phep mo rong them collection va model moi ma khong can tai kien truc toan bo he thong.
- NFR18: He thong phai duy tri van hanh on dinh khi tang so luong bang staging/mart theo roadmap Phase 2.
- NFR19: Kien truc phai ho tro nang cap dan tu single-tenant noi bo sang mo hinh tenant-ready khi can.
- NFR20: Nang luc van hanh phai mo rong theo khoi luong du lieu tang dan ma van giu duoc quality gate bat buoc.