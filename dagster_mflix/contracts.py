from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_TOP_LEVEL_FIELDS = {
    "contract",
    "version",
    "owner",
    "status",
    "updated_at",
    "datasets",
}

REQUIRED_DATASET_FIELDS = {
    "name",
    "schema",
    "grain",
    "keys",
    "columns",
    "status",
}


def load_contract(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def validate_contract_document(contract: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL_FIELDS - set(contract.keys())
    if missing:
        raise ValueError(f"Missing required top-level fields: {sorted(missing)}")

    if not isinstance(contract["datasets"], list) or not contract["datasets"]:
        raise ValueError("datasets must be a non-empty list")

    for dataset in contract["datasets"]:
        missing_dataset_fields = REQUIRED_DATASET_FIELDS - set(dataset.keys())
        if missing_dataset_fields:
            raise ValueError(
                f"Dataset {dataset.get('name', '<unknown>')} is missing fields: {sorted(missing_dataset_fields)}"
            )

        keys = dataset["keys"]
        if not isinstance(keys, dict) or "primary" not in keys:
            raise ValueError(f"Dataset {dataset['name']} must define keys.primary")

        if not isinstance(dataset["columns"], list) or not dataset["columns"]:
            raise ValueError(f"Dataset {dataset['name']} must define non-empty columns")


def detect_breaking_changes(old_contract: dict[str, Any], new_contract: dict[str, Any]) -> list[str]:
    old_datasets = {item["name"]: item for item in old_contract.get("datasets", [])}
    new_datasets = {item["name"]: item for item in new_contract.get("datasets", [])}

    changes: list[str] = []

    for dataset_name in sorted(old_datasets.keys() - new_datasets.keys()):
        changes.append(f"Removed dataset: {dataset_name}")

    for dataset_name in sorted(old_datasets.keys() & new_datasets.keys()):
        old_ds = old_datasets[dataset_name]
        new_ds = new_datasets[dataset_name]

        if old_ds.get("grain") != new_ds.get("grain"):
            changes.append(f"Changed grain for dataset: {dataset_name}")

        if old_ds.get("keys", {}).get("primary") != new_ds.get("keys", {}).get("primary"):
            changes.append(f"Changed primary keys for dataset: {dataset_name}")

        old_columns = {column["name"] for column in old_ds.get("columns", [])}
        new_columns = {column["name"] for column in new_ds.get("columns", [])}
        removed_columns = sorted(old_columns - new_columns)
        for column_name in removed_columns:
            changes.append(f"Removed column {column_name} from dataset: {dataset_name}")

    return changes


def enforce_version_policy(old_version: str, new_version: str, breaking_changes: list[str]) -> None:
    old_major, old_minor, old_patch = _parse_semver(old_version)
    new_major, new_minor, new_patch = _parse_semver(new_version)

    if (new_major, new_minor, new_patch) <= (old_major, old_minor, old_patch):
        raise ValueError("New contract version must be greater than old version")

    if breaking_changes and new_major <= old_major:
        raise ValueError("Breaking changes detected; major version bump is required")


def _parse_semver(version: str) -> tuple[int, int, int]:
    parts = version.strip().split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid semantic version: {version}")
    return int(parts[0]), int(parts[1]), int(parts[2])
