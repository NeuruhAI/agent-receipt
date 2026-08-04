# Test Report

Generated: 2026-08-04T14:33:57.942818+00:00

## Standard-library test suite

```text
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/generated/interface/models.py", line 30820, in hydrate_crdt_from_proto
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/rpc/remote.py", line 749, in __call__
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
test_broken_link_is_detected (test_receipts.ReceiptTests.test_broken_link_is_detected) ... ok
test_execution_cannot_claim_authorization (test_receipts.ReceiptTests.test_execution_cannot_claim_authorization) ... ok
test_external_tip_detects_truncation (test_receipts.ReceiptTests.test_external_tip_detects_truncation) ... ok
test_reorder_is_detected (test_receipts.ReceiptTests.test_reorder_is_detected) ... ok
test_tamper_is_detected (test_receipts.ReceiptTests.test_tamper_is_detected) ... ok
test_unknown_field_fails_closed (test_receipts.ReceiptTests.test_unknown_field_fails_closed) ... ok
test_valid_chain (test_receipts.ReceiptTests.test_valid_chain) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

Result: **PASS**

## CLI smoke test

```json
{
  "ok": true,
  "length": 3,
  "tip": "63a5bea04a74c7fb5dc52e71483a71eaa7bf1b6c8243444a9cc66904843f2eb3"
}
```

Result: **PASS**

These tests ran inside the packaging environment. The private staging launcher
runs them again on Jeramie's Mac before creating repositories.
