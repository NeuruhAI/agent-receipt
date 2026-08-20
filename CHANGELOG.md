# Changelog

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
