# Security Policy

## Scope

Neuruh Agent Receipt is a verification library and specification. It does not authorize actions, execute agents, manage credentials, verify identity, or provide a production trust root.

Security reports are especially useful when they involve:

- receipt-chain verification bypasses;
- tamper detection failures;
- truncation or reordering that is incorrectly accepted;
- authority-class confusion;
- parser behavior that causes invalid receipts to pass;
- unsafe assumptions in the documented security boundary.

## Reporting

Please report suspected vulnerabilities privately to the repository maintainers through GitHub's private vulnerability reporting feature when available. Do not include real customer data, credentials, private Neuruh infrastructure details, or exploit material unrelated to this repository.

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Explicit non-goals

This project does not claim to provide digital signatures, identity attestation, key management, authorization, secure execution, non-repudiation, or proof of real-world business outcomes.
