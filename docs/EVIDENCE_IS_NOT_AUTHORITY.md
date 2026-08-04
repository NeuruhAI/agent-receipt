# Evidence Is Not Authority

Agent infrastructure becomes unsafe and misleading when one receipt is allowed
to make every claim.

## Four separate claims

### Request

Someone or something asked for an operation.

### Governance decision

A decision boundary allowed, denied, or escalated the request.

### Execution evidence

An executor observed an operation and recorded its result.

### Outcome evidence

A separate observation indicates whether the larger objective was achieved.

## Non-upgrade rule

An execution record may prove that bytes were written, a request was sent, or
a tool returned. It may not declare that it authorized itself, that the human
approved it, or that the mission succeeded.

This package enforces that rule structurally for the fields it understands.

## Limits

Hash chains are tamper-evident, not magically trustworthy. They do not prove:

- who controlled the machine;
- whether the clock was accurate;
- whether omitted events occurred;
- whether the first receipt was truthful;
- whether an external outcome was correctly measured;
- whether keys or identities were secure.

Those questions require additional identity, signature, custody, and outcome
systems.
