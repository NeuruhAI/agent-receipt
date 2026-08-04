from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .canonical import canonical_json, sha256_hex

GENESIS = "NEURUH_AGENT_RECEIPT_GENESIS_V1"

RECEIPT_TYPES = {
    "decision",
    "execution",
    "observation",
    "outcome",
}

AUTHORITY_CLASSES = {
    "governance-decision",
    "execution-evidence",
    "observation",
    "outcome-evidence",
}

REQUIRED_FIELDS = {
    "schema_version",
    "seq",
    "receipt_type",
    "authority",
    "observed_at",
    "subject",
    "correlation_id",
    "causation_id",
    "payload",
    "prev_hash",
    "entry_hash",
}


class ReceiptValidationError(ValueError):
    """Named refusal for invalid or misleading receipt material."""


@dataclass(frozen=True)
class LedgerVerification:
    ok: bool
    length: int
    tip: str
    receipts: tuple[dict[str, Any], ...]


def _body(entry: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in entry.items() if key != "entry_hash"}


def entry_hash(entry_without_hash: Mapping[str, Any]) -> str:
    return sha256_hex(canonical_json(dict(entry_without_hash)))


def seal_entry(entry: Mapping[str, Any], *, prev_hash: str, seq: int) -> dict[str, Any]:
    body = dict(entry)
    body["seq"] = seq
    body["prev_hash"] = prev_hash
    body.pop("entry_hash", None)
    sealed = dict(body)
    sealed["entry_hash"] = entry_hash(body)
    return sealed


def _validate_shape(entry: Mapping[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(entry))
    if missing:
        raise ReceiptValidationError(f"missing required fields: {', '.join(missing)}")

    unknown = sorted(set(entry) - REQUIRED_FIELDS)
    if unknown:
        raise ReceiptValidationError(f"unknown fields: {', '.join(unknown)}")

    if entry["schema_version"] != "neuruh.agent-receipt.v1alpha1":
        raise ReceiptValidationError("unsupported schema_version")

    if not isinstance(entry["seq"], int) or entry["seq"] < 0:
        raise ReceiptValidationError("seq must be a non-negative integer")

    if entry["receipt_type"] not in RECEIPT_TYPES:
        raise ReceiptValidationError("unknown receipt_type")

    if entry["authority"] not in AUTHORITY_CLASSES:
        raise ReceiptValidationError("unknown authority class")

    for field in ("observed_at", "subject", "correlation_id", "causation_id"):
        if not isinstance(entry[field], str) or not entry[field]:
            raise ReceiptValidationError(f"{field} must be a non-empty string")

    if not isinstance(entry["payload"], dict):
        raise ReceiptValidationError("payload must be an object")

    for field in ("prev_hash", "entry_hash"):
        if not isinstance(entry[field], str) or not entry[field]:
            raise ReceiptValidationError(f"{field} must be a non-empty string")


def _validate_authority(entry: Mapping[str, Any]) -> None:
    authority = entry["authority"]
    receipt_type = entry["receipt_type"]
    payload = entry["payload"]

    expected = {
        "decision": "governance-decision",
        "execution": "execution-evidence",
        "observation": "observation",
        "outcome": "outcome-evidence",
    }[receipt_type]

    if authority != expected:
        raise ReceiptValidationError(
            f"receipt_type {receipt_type!r} requires authority {expected!r}"
        )

    if authority == "execution-evidence":
        forbidden_truthy = (
            "authorized",
            "mission_completed",
            "objective_completed",
            "business_outcome_proven",
        )
        claimed = [key for key in forbidden_truthy if payload.get(key) is True]
        if claimed:
            raise ReceiptValidationError(
                "execution evidence cannot upgrade itself into authority or "
                f"mission completion: {', '.join(claimed)}"
            )


def verify_entry(
    entry: Mapping[str, Any],
    *,
    expected_seq: int,
    expected_prev_hash: str,
) -> None:
    _validate_shape(entry)
    _validate_authority(entry)

    if entry["seq"] != expected_seq:
        raise ReceiptValidationError(
            f"sequence mismatch: expected {expected_seq}, got {entry['seq']}"
        )

    if entry["prev_hash"] != expected_prev_hash:
        raise ReceiptValidationError("previous-hash link mismatch")

    expected_hash = entry_hash(_body(entry))
    if entry["entry_hash"] != expected_hash:
        raise ReceiptValidationError("entry hash mismatch")


def verify_ledger(
    entries: Iterable[Mapping[str, Any]],
    *,
    expected_tip: str | None = None,
) -> LedgerVerification:
    previous = GENESIS
    verified: list[dict[str, Any]] = []

    for index, raw in enumerate(entries):
        entry = dict(raw)
        verify_entry(
            entry,
            expected_seq=index,
            expected_prev_hash=previous,
        )
        previous = entry["entry_hash"]
        verified.append(entry)

    tip = previous

    if expected_tip is not None and tip != expected_tip:
        raise ReceiptValidationError(
            "tip hash mismatch; ledger may be truncated or from a different run"
        )

    return LedgerVerification(
        ok=True,
        length=len(verified),
        tip=tip,
        receipts=tuple(verified),
    )


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    source = Path(path)

    with source.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ReceiptValidationError(
                    f"invalid JSON at line {line_number}: {exc.msg}"
                ) from exc
            if not isinstance(value, dict):
                raise ReceiptValidationError(
                    f"line {line_number} must contain a JSON object"
                )
            records.append(value)

    return records
