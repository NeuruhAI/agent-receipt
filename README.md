# Neuruh Agent Receipt

A small, dependency-free specification and verifier for portable,
tamper-evident agent receipts.

## Problem

Agent systems often blur four different claims:

1. A request existed.
2. A governance decision was issued.
3. Execution occurred.
4. The mission or business outcome succeeded.

Those claims are not interchangeable.

An execution receipt is evidence that an operation occurred. It is not
authorization, and it is not proof that the larger objective was completed.

## What this package provides

- A canonical receipt envelope
- Append-only SHA-256 hash-chain verification
- Sequence, insertion, reorder, and broken-link detection
- Optional external-tip verification for tail truncation
- Explicit authority classes
- Synthetic examples
- A dependency-free command-line verifier
- A standard-library test suite

## What it does not provide

- A policy engine
- Production authorization
- Agent execution
- Identity verification
- Cryptographic signatures
- Key management
- A database
- Proof that a real-world outcome occurred

## Quick start

```bash
python3 -m unittest discover -s tests -v

PYTHONPATH=src python3 -m neuruh_agent_receipt.cli   verify examples/valid-ledger.jsonl   --expected-tip-file examples/valid-tip.txt
```

## Authority classes

- `governance-decision`
- `execution-evidence`
- `observation`
- `outcome-evidence`

The verifier refuses an `execution-evidence` receipt whose payload claims that
it authorized an action or completed a higher-level mission.

## Status

**Active Alpha / private staging candidate.**

The format is intentionally narrow. It should be tested in public before
stability claims are made.
