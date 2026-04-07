from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dagster import AssetExecutionContext, AssetKey, Failure, asset


REPO_ROOT = Path(__file__).resolve().parents[2]
SODA_CONFIG = REPO_ROOT / "soda" / "configuration" / "configuration.yml"
DBT_MANIFEST = REPO_ROOT / "mflix_snowflake" / "target" / "manifest.json"
SODA_CHECKS = {
    "raw": {
        "datasource": "snowflake_raw",
        "files": [REPO_ROOT / "soda" / "checks" / "check_ingest_raw.yml"],
    },
    "staging": {
        "datasource": "snowflake_analytics",
        "files": [REPO_ROOT / "soda" / "checks" / "check_staging.yml"],
    },
    "transform": {
        "datasource": "snowflake_analytics",
        "files": [REPO_ROOT / "soda" / "checks" / "check_transform.yml"],
    },
    "report": {
        "datasource": "snowflake_analytics",
        "files": [REPO_ROOT / "soda" / "checks" / "check_report.yml"],
    },
    "anomaly": {
        "datasource": "snowflake_analytics",
        "files": [REPO_ROOT / "soda" / "checks" / "check_anomaly.yml"],
    },
}

RAW_ASSET_KEYS = [
    AssetKey(["raw", "dlt_mongodb_comments"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__genres"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__cast"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__countries"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__directors"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__writers"]),
    AssetKey(["raw", "dlt_mongodb_embedded_movies__languages"]),
]

STAGING_ASSET_KEYS = [
    "stg_comments",
    "stg_embedded_movies",
    "stg_movie_cast",
    "stg_movie_genres",
    "stg_movie_countries",
    "stg_movie_directors",
    "stg_movie_writers",
    "stg_movie_languages",
]

INTERMEDIATE_ASSET_KEYS = [
    "int_movie_flattened",
    "int_movie_genres_bridge",
    "int_movie_countries_bridge",
    "int_movie_cast_bridge",
    "int_movie_directors_bridge",
    "int_movie_languages_bridge",
    "int_movie_writers_bridge",
]

REPORT_ASSET_KEYS = [
    "fct_movie_engagement",
    "agg_top_movies_by_month",
    "agg_top_movies_by_engagement",
    "fct_movie_quality",
]

ANOMALY_ASSET_KEYS = [
    "stg_comments",
    "fct_movie_consumption_daily",
    "fct_movie_engagement",
]


def _run_soda_scan(datasource: str, check_files: list[Path]) -> dict[str, Any]:
    command = [
        "soda",
        "scan",
        "-d",
        datasource,
        "-c",
        str(SODA_CONFIG),
        *[str(path) for path in check_files],
    ]
    proc = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-8000:],
        "stderr": proc.stderr[-8000:],
    }


def _hash_file(path: Path) -> str | None:
    if not path.exists():
        return None

    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _git_sha() -> str | None:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _layer_audit_context(context: AssetExecutionContext, layer: str, scan_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": context.run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "layer": layer,
        "quality_status": "passed",
        "git_sha": _git_sha(),
        "dbt_manifest_sha256": _hash_file(DBT_MANIFEST),
        "soda_command": scan_result["command"],
        "soda_stdout_tail": scan_result["stdout"],
        "soda_stderr_tail": scan_result["stderr"],
    }


def _write_layer_audit(context: AssetExecutionContext, layer: str, payload: dict[str, Any]) -> Path:
    audit_dir = REPO_ROOT / "logs" / "quality_audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_file = audit_dir / f"{context.run_id}-{layer}.json"
    audit_file.write_text(json.dumps(payload, indent=2, ensure_ascii=True))
    return audit_file


def _execute_layer_gate(context: AssetExecutionContext, layer: str) -> None:
    layer_config = SODA_CHECKS[layer]
    soda_result = _run_soda_scan(layer_config["datasource"], layer_config["files"])
    if soda_result["returncode"] != 0:
        raise Failure(
            description=f"Soda checks failed for {layer} layer. Blocking publish.",
            metadata={
                "layer": layer,
                "soda_stdout_tail": soda_result["stdout"],
                "soda_stderr_tail": soda_result["stderr"],
            },
        )

    audit_payload = _layer_audit_context(context, layer, soda_result)
    audit_file = _write_layer_audit(context, layer, audit_payload)
    context.log.info(f"Quality gate passed for {layer} layer. Audit written to {audit_file}")


def _make_layer_quality_gate(asset_name: str, layer: str, deps: list[str]):
    @asset(name=asset_name, group_name="quality", deps=deps)
    def _layer_quality_gate(context) -> None:
        _execute_layer_gate(context, layer)

    return _layer_quality_gate


raw_quality_gate = _make_layer_quality_gate("raw_quality_gate", "raw", RAW_ASSET_KEYS)
staging_quality_gate = _make_layer_quality_gate(
    "staging_quality_gate",
    "staging",
    ["raw_quality_gate", *STAGING_ASSET_KEYS],
)
transform_quality_gate = _make_layer_quality_gate(
    "transform_quality_gate",
    "transform",
    ["staging_quality_gate", *INTERMEDIATE_ASSET_KEYS],
)
report_quality_gate = _make_layer_quality_gate(
    "report_quality_gate",
    "report",
    ["transform_quality_gate", *REPORT_ASSET_KEYS],
)
anomaly_quality_gate = _make_layer_quality_gate(
    "anomaly_quality_gate",
    "anomaly",
    ["report_quality_gate", *ANOMALY_ASSET_KEYS],
)
