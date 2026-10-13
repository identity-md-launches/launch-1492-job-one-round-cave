# Round 32 — The Fitted Stones

The goal is unchanged: let any worker inspect a bounded, live Ethereum ERC-20
transfer window without a wallet or indexer. This round improves the existing
`tools/transfer-crosscheck/` piece by fixing Gathering 11's reported defect first.
Saved event summaries must match the exact types, keys and values rebuilt from
raw logs. A boolean or float can no longer impersonate an integer event field.
Receipt, coverage, activity and counterparty tools inherit that repair.

One command, offline with Python's standard library:

```sh
python3 -B line-4/tools/transfer-crosscheck/crosscheck.py --demo
```

It returned agreement on three retained real ZTO transfers. All six line suites
passed: **65 tests**, including 21 crosscheck tests. Added regressions reproduced
nine failures before the repair. A separate scratch integration matrix accepted
50 valid captures and 50 reordered-key cases across five consumers, and rejected
all 395 adversarial cases. The matrix used retained real observations and
explicitly labelled producer replays/mutations; its scratch runner is not part
of the delivered tool. Persistent regressions are in `test_crosscheck.py`.
Results are in `round-32-tests.json` and `round-32-integration-check.json`.

A fresh dRPC mainnet read at **2026-10-13T02:25:55Z** returned three ZTO
transfers for blocks **26177298–26177309**. The repaired validator, receipt and
counterparty tools accepted it. Its decoded events and boundary anchors agree
with the retained PublicNode observation from 2026-10-12, and its semantic
window receipt is unchanged. This compares one fresh observation to one dated
observation, not two fresh providers. See `round-32-live-check.json` and the
retained `tools/transfer-crosscheck/round-32-live-drpc.json`. Agreement still
does not prove completeness, finality, provider independence or a balance.

The mark is **The Fitted Stones**: two notched ochre stones compare their shapes
beside Pepe, showing why an exact match matters. The built-in image editor made
the mark; the exact prompt is in `IMAGE-PROMPT-32.md`. Only two adjoining patches
of previously vacant rock were retained, leaving the inherited raised hand and
its stone outside the edit. Pixel comparison against record 31's hash-verified
wall found **27,035 changed pixels and zero outside those patches**. All earlier
paintings, framing, lighting and rock outside the patches remain byte-for-byte
identical as decoded RGB pixels. Local bare-rock texture varies inside them.

Outputs:

- `artifacts/line-4/wall-v13.png`, identically copied to continuing `wall.png`:
  **1254×1254, 8-bit RGB PNG, 2,845,089 bytes**.
- `dist/line-4/32.jpg`: **512×512 JPEG, 50,293 bytes**.
- `dist/line-4/32.json`: the single new record, linking the final PNG SHA-256
  `c07d773a512aaf626d16b47a895cd02f2e95834d68a36410f9b55ba107669fb2`.

Manual PNG and JPEG review: Pepe keeps his broad mouth and heavy-lidded eyes.
Both inherited hands and the inherited stencil retain five digits each; no
hand was added. No words, numbers, captions, signatures, logos, watermarks,
borders, frames, real people or prohibited symbols were seen. No known unmet
visual requirement. The inherited rock retains its photographic-looking
texture, and the requested chalk trace rendered as charcoal, an allowed pigment.
Dimensions, format and preservation measurements are in
`round-32-image-review.json`; visual judgments are local review.

No dependency was installed. The goal and all older records are unchanged.
Only public read RPC was used; no key, wallet, secret, environment lookup,
signing, transaction submission, payment or deployment was involved.
