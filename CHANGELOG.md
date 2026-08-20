# Changelog

## 0.1.2a0 — v0.1.2-alpha

- `__version__` is now read from installed distribution metadata instead of a hard-coded
  literal, which had drifted from `pyproject.toml` in v0.1.1-alpha.
- No other change. Use this tag rather than v0.1.1-alpha.

## 0.1.1a0 — v0.1.1-alpha

- First tagged release. Earlier consumers pinned a raw commit SHA; they should move to `v0.1.1-alpha`.
- Packaging metadata: PEP 639 `license`/`license-files`, project URLs, schema data files.
- README documents install, verification with expected output, the public API, and the evidence-is-not-authority boundary.
- Continuous integration on Python 3.11, 3.12, and 3.13.
- No behavioral change to receipt sealing or verification.

## 0.1.0

- Initial receipt envelope
- Dependency-free verifier
- Authority separation
- Synthetic examples
- Tamper, reorder, truncation, link, and false-authority tests
