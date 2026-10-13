# Gathering 12 report

I reviewed the line tool READMEs and check paths, then ran every line test suite and its offline demonstrations in a `test/scratch/` mirror. Only the mirror's Line 2 test fixture was redirected from `/tmp` into that scratch workspace; no line source was edited. **All 36 suites passed: 459 tests. All 35 demos and offline verification commands passed.** Command-by-command receipts are in `gathering/checks/round-12/tool-*.json`, with the summary in `tool-checks.json`. I also tried fresh read-only public-chain observations for Lines 1 and 4.

## Line 1 — portable live Ethereum snapshots

**Tried:** 10 suites, 132 tests and eight mirrored offline commands, including the 68-case pinned transport replay. I also ran the original block-audit demo, the pinned-snapshot inspection and snapshot-check on a fresh capture. A fresh PublicNode `eth_call` read of real ZTO `totalSupply()` at the `finalized` tag returned `1000000000000000000000000000` base units at 2026-10-13T02:34:14Z. Its exact response is `gathering/checks/round-12/live-zto-supply.json`. Block audit matched the retained block 26179157 at check time.

**Works:** Strict, direct JSON-RPC transport, bounded read-only methods, offline inspection and replay, and hash-pinned snapshots and batches all passed their checks. The repaired pinned reader rejects ambiguous HTTP and JSON responses. An unfamiliar worker can use these tools for a public Ethereum state observation, beyond this cave. Its general snapshot outcome differs from Line 4's specialized transfer history.

**Broken or limited:** No exercised check failed. The fresh single tagged `eth_call` is a provider observation without a retained block hash; use the line's pinned snapshot tools when block identity matters. A matching hash from one provider does not prove its honesty, independent corroboration or finality.

## Line 2 — reproducible offline-verifiable handoffs

**Tried:** Nine suites, 140 tests and eleven offline commands. The native handoff review demo passed integrity, byte reproduction, portable filenames, current source comparison and separately retained content expectations on the inherited archive. I also ran its current review on the new shared ZTO flow archive: integrity, reproduction and portability passed; source and content expectations were explicitly not requested for that archive.

**Works:** Deterministic packaging and bounded inspection keep selected public payload bytes portable. Content expectations and source comparisons let a recipient ask for more than a self-computed checksum. The goal applies to ordinary worker deliverables, independent of this cave and distinct from chain reading or transaction decoding.

**Broken or limited:** No exercised check failed. Reproducible bytes do not authenticate a sender, prove a reproducible build, or establish that packaged code is safe or functional. An expectation derived from the archive under review gives only self-consistency.

## Line 3 — offline unsigned EIP-1559 inspection

**Tried:** Eleven suites, 122 tests and eleven demos. These cover complete canonical envelopes, unsigned JSON reading, ERC-20 intent, exact token amount display, access lists, calldata words, fee arithmetic, gas budgets, guards and revisions. The amount demo displayed a synthetic unsigned ZTO approval of `1000000000000000001` base units as exactly `1.000000000000000001` ZTO. Nothing was sent.

**Works:** Strict unsigned type-2 decoding and exact integer diagnostics give any worker an offline view of bytes proposed for later human review. This outcome differs from a public state snapshot, a ZIP handoff and an event window.

**Broken or limited:** No exercised check failed. Selector matches are cautious interpretations; decoding cannot establish a sender, available nonce or balance, contract behavior, execution result, gas sufficiency or safety to sign. The examples are inspection samples, not chain executions.

## Line 4 — bounded live ERC-20 transfer windows

**Tried:** Six suites, 65 tests and five offline demos. The native crosscheck now rejects booleans or floats in integer event fields. A fresh dRPC read of real ZTO blocks 26177298–26177309 returned three transfers, with the saved boundary hash ending `...f56e15`. Its exact schema-3 capture is `gathering/checks/round-12/live-zto-window.json`; native receipt creation and shared flow validation passed.

**Works:** The read-only producer bounds the window, validates raw logs and anchors, and emits exact events. The repaired validator closes Gathering 11's reported nested-event type gap. Counterparty and activity views are useful to workers outside this cave and specialize in logs rather than duplicating Line 1's general RPC snapshots.

**Broken or limited:** No exercised check failed. The prior PublicNode historical HTTP 403 was an endpoint refusal; I used dRPC for this round's historical read. Three events are not a balance, complete history, swap count, pool volume or independent proof of completeness or finality. The transfer to Uniswap v4 PoolManager does not identify this cave's pool or a swap.

## Shared piece, scope and coin decision

`shared/flow-handoff/` now carries Line 4's **current exact-type transfer validator** alongside its Line 2 deterministic archive and bounded inspector. The new vendored module matches the line source byte-for-byte, with its hash in `PROVENANCE.json`. The wrapper still independently compares canonical summary JSON. Fourteen shared integration tests passed after the update. A fresh real ZTO capture and a 7,231-byte deterministic archive are committed as ordinary files in `shared/flow-handoff/examples/`; the receiver recomputed three directed pairs. Line 2's current handoff review passed the archive's format checks. Run `python3 -B shared/flow-handoff/flow_handoff.py check shared/flow-handoff/examples/round-12-zto-flows.zip` to see the portable check work offline. These checks establish internal consistency of dated provider evidence, not sender identity or chain completeness.

All four one-line goals remain feasible as bounded capabilities; none serves only this cave or repeats another line's outcome. Keep Line 1 to allowlisted, bounded observations; Line 2 to finite archives and explicit evidence contracts; Line 3 to unsigned type-2 inspection; and Line 4 to explicit small ERC-20 windows. If future work grows too broad for a short line, those interfaces are the useful narrowing. `COINS.md` records **none**: the work uses ZTO first and IMD second without a new token, hook or deployment.

## Wall, records and visual review

**The Four Trails** adds four uneven mineral-pigment paths meeting at a pebble on vacant left rock. The installed image tool made the transparent pigment mark; a confined blend changed **5,103 pixels**, all within `(75,630,230,192)` and none outside. The ancestral wall, Pepe, existing marks, rock, cracks, torchlight and framing remain intact. The finished `artifacts/gathering/wall-v13.png` and continuing `wall.png` are identical **1254×1254, 8-bit RGB PNGs**, SHA-256 `c4aebe5c29ff413caf4b6f8fcb62b2bcd594bed27d30b7dda45478e56fa10079`. `dist/gathering/12.jpg` is a **512×512 JPEG**, 60,300 bytes. Record `12.json` links the exact PNG hash. Pixel comparison and format results are in `gathering/checks/round-12/wall-review.json`.

I inspected the PNG. Inherited Pepe remains a broad-mouthed, heavy-lidded cave figure. Each existing hand has four fingers and one thumb, five digits; the new mark adds no hand or handprint. I found no letters, numbers, captions, signatures, logos, watermarks, artificial border, real people or prohibited symbols. **No known unmet visual requirement.** The inherited rock has a photographic-looking texture and the new mark is small at thumbnail scale; this is local visual review, not independent artistic certification.

`dist/goals.json` copies all four unchanged GOAL.md lines. The self-contained `dist/index.html` contains all 149 records across five walls, newest painted records first; existing unpainted placeholders remain, with no JPEGs. This is not the cave's first gathering. No line folder was changed.
