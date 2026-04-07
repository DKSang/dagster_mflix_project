from pathlib import Path
import importlib.util

import pytest
import yaml


_MODULE_PATH = Path("dagster_mflix/contracts.py")
_SPEC = importlib.util.spec_from_file_location("contracts", _MODULE_PATH)
assert _SPEC and _SPEC.loader
_CONTRACTS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_CONTRACTS)

detect_breaking_changes = _CONTRACTS.detect_breaking_changes
enforce_version_policy = _CONTRACTS.enforce_version_policy
validate_contract_document = _CONTRACTS.validate_contract_document


def _load_contract(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_contract_has_required_top_level_fields() -> None:
    contract = _load_contract(Path("data_contracts/mart_contracts.yml"))
    validate_contract_document(contract)


def test_contract_datasets_exist_in_dbt_schema() -> None:
    contract = _load_contract(Path("data_contracts/mart_contracts.yml"))
    dbt_schema = yaml.safe_load(Path("mflix_snowflake/models/marts/schema.yml").read_text(encoding="utf-8"))

    dbt_model_names = {model["name"] for model in dbt_schema.get("models", [])}
    for dataset in contract["datasets"]:
        assert dataset["name"] in dbt_model_names


def test_breaking_change_requires_major_version_bump() -> None:
    old_contract = {
        "version": "1.2.0",
        "datasets": [
            {
                "name": "fct_movie_engagement",
                "schema": "MART",
                "grain": "one row per movie_id",
                "keys": {"primary": ["movie_id"]},
                "columns": [{"name": "movie_id"}, {"name": "engagement_score"}],
            }
        ],
    }
    new_contract = {
        "version": "1.3.0",
        "datasets": [
            {
                "name": "fct_movie_engagement",
                "schema": "MART",
                "grain": "one row per movie_id",
                "keys": {"primary": ["movie_id"]},
                "columns": [{"name": "movie_id"}],
            }
        ],
    }

    changes = detect_breaking_changes(old_contract, new_contract)
    assert changes

    with pytest.raises(ValueError):
        enforce_version_policy(old_contract["version"], new_contract["version"], changes)


def test_non_breaking_change_allows_minor_bump() -> None:
    old_contract = {
        "version": "1.2.0",
        "datasets": [
            {
                "name": "fct_movie_engagement",
                "schema": "MART",
                "grain": "one row per movie_id",
                "keys": {"primary": ["movie_id"]},
                "columns": [{"name": "movie_id"}],
            }
        ],
    }
    new_contract = {
        "version": "1.3.0",
        "datasets": [
            {
                "name": "fct_movie_engagement",
                "schema": "MART",
                "grain": "one row per movie_id",
                "keys": {"primary": ["movie_id"]},
                "columns": [{"name": "movie_id"}, {"name": "engagement_score"}],
            }
        ],
    }

    changes = detect_breaking_changes(old_contract, new_contract)
    assert not changes
    enforce_version_policy(old_contract["version"], new_contract["version"], changes)