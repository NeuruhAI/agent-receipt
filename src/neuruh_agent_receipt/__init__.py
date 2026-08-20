from .canonical import canonical_json, sha256_hex
from .ledger import (
    GENESIS,
    ReceiptValidationError,
    entry_hash,
    seal_entry,
    verify_entry,
    verify_ledger,
)

__all__ = [
    "GENESIS",
    "ReceiptValidationError",
    "canonical_json",
    "sha256_hex",
    "entry_hash",
    "seal_entry",
    "verify_entry",
    "verify_ledger",
]

from importlib.metadata import PackageNotFoundError, version as _metadata_version

try:
    __version__ = _metadata_version("neuruh-agent-receipt")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "unknown"
