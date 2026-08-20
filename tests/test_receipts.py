from __future__ import annotations

import copy
import unittest
from pathlib import Path

from neuruh_agent_receipt.ledger import (
    GENESIS,
    ReceiptValidationError,
    load_jsonl,
    seal_entry,
    verify_ledger,
)

ROOT = Path(__file__).resolve().parents[1]


class ReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = load_jsonl(ROOT / "examples" / "valid-ledger.jsonl")
        self.tip = (ROOT / "examples" / "valid-tip.txt").read_text().strip()

    def test_valid_chain(self) -> None:
        result = verify_ledger(self.entries, expected_tip=self.tip)
        self.assertTrue(result.ok)
        self.assertEqual(result.length, 3)
        self.assertEqual(result.tip, self.tip)

    def test_tamper_is_detected(self) -> None:
        entries = copy.deepcopy(self.entries)
        entries[1]["payload"]["bytes_written"] = 999
        with self.assertRaisesRegex(ReceiptValidationError, "entry hash mismatch"):
            verify_ledger(entries)

    def test_reorder_is_detected(self) -> None:
        entries = copy.deepcopy(self.entries)
        entries[0], entries[1] = entries[1], entries[0]
        with self.assertRaises(ReceiptValidationError):
            verify_ledger(entries)

    def test_broken_link_is_detected(self) -> None:
        entries = copy.deepcopy(self.entries)
        entries[2]["prev_hash"] = GENESIS
        entries[2] = seal_entry(
            {
                key: value
                for key, value in entries[2].items()
                if key not in {"seq", "prev_hash", "entry_hash"}
            },
            prev_hash=GENESIS,
            seq=2,
        )
        with self.assertRaisesRegex(
            ReceiptValidationError,
            "previous-hash link mismatch",
        ):
            verify_ledger(entries)

    def test_external_tip_detects_truncation(self) -> None:
        truncated = copy.deepcopy(self.entries[:-1])
        with self.assertRaisesRegex(ReceiptValidationError, "tip hash mismatch"):
            verify_ledger(truncated, expected_tip=self.tip)

    def test_execution_cannot_claim_authorization(self) -> None:
        entries = load_jsonl(ROOT / "examples" / "false-authority-ledger.jsonl")
        with self.assertRaisesRegex(
            ReceiptValidationError,
            "cannot upgrade itself",
        ):
            verify_ledger(entries)

    def test_unknown_field_fails_closed(self) -> None:
        entries = copy.deepcopy(self.entries)
        entries[0]["surprise"] = "not allowed"
        with self.assertRaisesRegex(ReceiptValidationError, "unknown fields"):
            verify_ledger(entries)


if __name__ == "__main__":
    unittest.main()
