#!/usr/bin/env python3
import json, pathlib, sys
base=pathlib.Path(__file__).resolve().parents[1]/"contracts/estate-wave-01"
files=list(base.glob("*.json"))
assert files
for p in files:
    c=json.loads(p.read_text())
    assert c["authority_effect"]=="none"
    assert c["write_capabilities"]==[]
    assert c["production_mutation_allowed"] is False
    assert c["deployment_authorized"] is False
    assert c["publication_authorized"] is False
    assert c["visibility_change_authorized"] is False
print(f"PASS {len(files)} Wave 01 contract(s)")
sys.exit(0)
