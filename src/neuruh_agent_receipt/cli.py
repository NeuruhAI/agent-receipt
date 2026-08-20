from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .ledger import ReceiptValidationError, load_jsonl, verify_ledger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neuruh-agent-receipt",
        description="Verify a Neuruh Agent Receipt JSONL hash chain.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="verify a JSONL receipt ledger")
    verify.add_argument("ledger")
    verify.add_argument("--expected-tip")
    verify.add_argument("--expected-tip-file")
    verify.add_argument("--json", action="store_true", dest="json_output")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "verify":
        expected_tip = args.expected_tip

        if args.expected_tip_file:
            if expected_tip:
                print(
                    "Use only one of --expected-tip or --expected-tip-file.",
                    file=sys.stderr,
                )
                return 2
            expected_tip = (
                Path(args.expected_tip_file).read_text(encoding="utf-8").strip()
            )

        try:
            entries = load_jsonl(args.ledger)
            result = verify_ledger(entries, expected_tip=expected_tip)
        except (OSError, ReceiptValidationError) as exc:
            if args.json_output:
                print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
            else:
                print(f"FAIL: {exc}", file=sys.stderr)
            return 1

        payload = {
            "ok": result.ok,
            "length": result.length,
            "tip": result.tip,
        }

        if args.json_output:
            print(json.dumps(payload, indent=2))
        else:
            print(f"PASS: {result.length} receipts")
            print(f"TIP: {result.tip}")

        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
