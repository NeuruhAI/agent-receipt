# Neuruh Agent Receipt

A dependency-free specification and verifier for portable, tamper-evident agent receipts.

An agent receipt records one observation about a run. Hash chaining makes insertion, reordering, broken links, and optional tail truncation detectable.

## Install

```bash
git clone https://github.com/NeuruhAI/agent-receipt.git
cd agent-receipt
python -m venv .venv
source .venv/bin/activate
pip install .
```

Or install a pinned release directly:

```bash
pip install "neuruh-agent-receipt @ git+https://github.com/NeuruhAI/agent-receipt.git@v0.1.2-alpha"
```

## Verify a ledger

```bash
neuruh-agent-receipt verify examples/valid-ledger.jsonl \
  --expected-tip-file examples/valid-tip.txt
```

Expected output:

```text
PASS: 3 receipts
TIP: 63a5bea04a74c7fb5dc52e71483a71eaa7bf1b6c8243444a9cc66904843f2eb3
```

The verifier exits nonzero for malformed receipts, invalid authority claims, sequence gaps, changed entries, broken links, or a ledger tip that does not match the separately stored expected tip. The repository ships `examples/tampered-ledger.jsonl` and `examples/false-authority-ledger.jsonl` so both failure paths can be reproduced.

Receipt authority classes are `governance-decision`, `execution-evidence`, `observation`, and `outcome-evidence`. The verifier rejects an execution receipt that claims it authorized an action or completed the higher-level mission.

## API

| Name | Purpose |
| --- | --- |
| `GENESIS` | `NEURUH_AGENT_RECEIPT_GENESIS_V1`, the previous-hash value of entry 0. |
| `seal_entry(entry, *, prev_hash, seq)` | Return the entry with its sequence, link, and `entry_hash`. |
| `entry_hash(entry_without_hash)` | Digest over the canonical entry body. |
| `verify_entry(entry, *, expected_seq, expected_prev_hash)` | Check one entry; raises on failure. |
| `verify_ledger(entries, *, expected_tip=None)` | Check a whole chain; returns a `LedgerVerification`. |
| `canonical_json(value)`, `sha256_hex(value)` | Deterministic serialization and hashing helpers. |
| `ReceiptValidationError` | Raised for every rejection. |

## Test

```bash
python -m unittest discover -s tests -v
```

## Safety boundary

Receipts are evidence, not authorization, identity proof, cryptographic signatures, or proof of a real-world outcome. Hash chaining detects tampering by someone who cannot rewrite the whole ledger and the separately stored tip; it does not prove who wrote an entry. Storing the expected tip somewhere the ledger writer cannot reach is what makes tail truncation detectable.

See [`docs/EVIDENCE_IS_NOT_AUTHORITY.md`](docs/EVIDENCE_IS_NOT_AUTHORITY.md) and the [Neuruh Public Commons boundary](https://github.com/NeuruhAI/public-commons/blob/main/PUBLIC_PRIVATE_BOUNDARY.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
