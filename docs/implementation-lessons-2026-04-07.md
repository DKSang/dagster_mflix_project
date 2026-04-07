# Retrospective Trien Khai Dagster + dbt + Soda (2026-04-07)

## 1) Van de phu thuoc asset khong dung (chay song song ngoai y muon)

- Trieu chung:
	- `mongodb`, `raw_quality_gate`, `dbt_staging` co luc bi scheduler cho chay song song.
- Nguyen nhan goc:
	- `@dbt_assets` khong nhan `deps` truc tiep.
	- Graph dbt chua co canh upstream toi `raw_quality_gate`.
- Cach xu ly da ap dung:
	- Tao source ky thuat trong `models/staging/source.yml`: `dagster_quality.raw_quality_gate`.
	- Gan `meta.dagster.asset_key: [raw_quality_gate]` cho source ky thuat nay.
	- Them vao tung model staging:
		- `-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}`
- Bai hoc:
	- Voi dbt asset, dependency phai di qua dbt graph (source/ref/depends_on), khong dat ky vong vao `deps` cua decorator.

## 2) Lech asset key giua DLT va dbt source

- Trieu chung:
	- Quality gate va dbt source khong noi duoc dung upstream, lineage bi sai.
- Nguyen nhan goc:
	- Key thuc te cua DLT la dang `dlt_mongodb_*` (duoc prefix va translator map), nhung source dbt dang map theo ten raw table thong thuong.
- Cach xu ly da ap dung:
	- Cap nhat `models/staging/source.yml` de map asset key chinh xac:
		- `[raw, dlt_mongodb_comments]`
		- `[raw, dlt_mongodb_embedded_movies]`
		- ... cac bang nested tuong ung.
	- Dong bo `RAW_ASSET_KEYS` trong quality gate theo cung key thuc te.
- Bai hoc:
	- Truoc khi noi dependency, phai in/kiem tra key asset thuc te cua nguon (DLT/dbt translator), tranh doan ten.

## 3) Kho khan khi verify asset graph bang import `defs`

- Trieu chung:
	- `uv run python ... from dagster_mflix import defs` bi fail khi load module.
- Nguyen nhan goc:
	- DLT source can `connection_url` va secrets, moi truong local khong co.
- Cach xu ly da ap dung:
	- Verify bang huong an thay the:
		- `uv run dbt parse`
		- Kiem tra `target/manifest.json` (parent_map/child_map) de xac nhan canh `raw_quality_gate -> stg_*`.
- Bai hoc:
	- Tach "verify graph" thanh 2 lop:
		- Lop dbt: parse + inspect manifest.
		- Lop Dagster runtime: chi chay khi env credentials day du.

## 4) Tooling/command pitfalls

- Van de da gap:
	- `rg` khong co san trong may => phai fallback qua `grep`.
	- Co run dbt tu sai thu muc (thieu `dbt_project.yml` o root) trong mot so lan test thu cong.
- Bai hoc:
	- Chuan hoa command:
		- Luon uu tien `uv run dbt ... --project-dir mflix_snowflake` hoac `cd mflix_snowflake` truoc.
	- Co fallback command strategy khi thieu binary (`rg` -> `grep -R`).

## 5) Nhieu file tam/thay doi khong lien quan trong working tree

- Van de da gap:
	- Nhieu file tam (`__pycache__`, sqlite dagster tmp, log artifacts, html/docx test) lam noisy diff.
- Bai hoc:
	- Tach bien doi chuc nang va artifact runtime.
	- Tang cuong `.gitignore` cho thu muc tam va output tool.
	- Khi review, uu tien thay doi file nguon lien quan truc tiep.

## 6) Kinh nghiem tich hop Soda + dbt + Dagster

- Nguyen tac:
	- dbt: chiu trach nhiem transform + test mo hinh.
	- Soda gate: chot cua chat luong theo layer (raw/staging/transform/report/anomaly) truoc khi publish tiep.
- Thuc hanh tot:
	- Giu check Soda khong trung lap hard-constraint voi dbt test.
	- Ghi audit file (run_id, layer, command, stdout/stderr tail) de truy vet nhanh.
	- Dat dependency theo thu tu:
		- raw assets -> `raw_quality_gate` -> dbt staging assets -> staging/transform/report gates.

## 7) Checklist cho lan trien khai sau

1. Xac nhan key asset thuc te cua DLT/dbt translator truoc khi wiring dependency.
2. Neu can phu thuoc vao asset ngoai dbt, dung `source.yml` + `meta.dagster.asset_key` + `depends_on`.
3. Chay `uv run dbt parse` sau moi thay doi graph.
4. Doc `target/manifest.json` de kiem tra parent_map/child_map cua model quan trong.
5. Chi verify Dagster runtime khi env secrets day du.
6. Chuan hoa command voi `uv` va `--project-dir`.
7. Don dep artifact tam truoc khi tao PR/deploy.

## 8) Quyet dinh ky thuat da chot

- Khong tim cach ep `deps` truc tiep vao `@dbt_assets`.
- Chon cach chuan theo dbt graph metadata.
- Chon source ky thuat `dagster_quality.raw_quality_gate` de noi dependency chat luong vao cac model staging.

