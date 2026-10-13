# Transfer crosscheck

Compare one bounded ERC-20 transfer window through two public Ethereum RPC
providers. ZTO is the default; IMD is available with `--token imd`. This companion
uses the ancestor's validated reader, fixes the same inclusive block range for
both providers, and compares token identity, pinned decimals, boundary hashes,
and every decoded event. It reports events seen only on one side and conflicting
events occupying the same block/log position. Each capture is revalidated from
its raw logs before its summary is trusted. Duplicate delivery and log order do
not create false differences.

One command to see it work **offline**, with no installation:

```sh
python3 -B line-4/tools/transfer-crosscheck/crosscheck.py --demo
```

Tried on 2026-10-12: it returned `agreement` for three real ZTO transfers in
blocks 26177298–26177309. `publicnode.json` and `drpc.json` are unchanged copies
of round 22's dated public-chain observations, not synthetic demo transactions.
The output retains both complete captures so the result can be inspected offline.
Python's standard library is the only dependency. Run from the repository root;
keep the sibling `erc20-transfer-window/` directory with this tool.

For a new observation:

```sh
python3 -B line-4/tools/transfer-crosscheck/crosscheck.py
```

This first observes PublicNode's mainnet head, chooses a 12-block window ending
12 blocks below it, then reads that exact range separately from PublicNode and
dRPC. Each reader checks its own head, mainnet chain ID and boundary stability.
The confirmation distance reduces moving-head races; it does not certify finality.
`--blocks 24 --confirmations 32` adjusts the selection. An explicit historical
range uses `--from-block N --to-block M` (1–2000 inclusive blocks). `--left-rpc`
and `--right-rpc` accept different credential-free public HTTPS RPC URLs.
Different URLs do not prove independent infrastructure.

The inherited reader also accepts the exact worker-supplied loopback mainnet
route `http://127.0.0.1:<port>/rpc/1` on either side. Both endpoints still have
to differ, and the read-only allowlist applies to both.

Exit codes: **0** means agreement, **1** means valid observations disagree,
**2** means invalid arguments, malformed evidence, reorg detection, resource
limits or provider failure. A provider error is never converted to an empty
successful window; partial success does not produce an agreement report.
Disagreements preserve both sides instead of silently merging them. No wallet,
key, environment variable, transaction signing or broadcasting is used. The
transport makes JSON-RPC POST requests solely for the ancestor's allowed public
read methods, with its dedicated User-Agent.

The live default command returned agreement for **zero** ZTO transfers in blocks
**26177570–26177581**, captured at **2026-10-12T16:29:28Z** and
**2026-10-12T16:29:37Z**. `live-zto.json` retains those two actual observations.
An agreed empty window is still only two provider observations. Agreement cannot
prove completeness, provider independence, finality, or an address's balance.
This tool inspects a window; it does not reconstruct balances or build an indexer.

Validation command:

```sh
python3 -B line-4/tools/transfer-crosscheck/test_crosscheck.py
```

All twelve offline tests passed: real three-event agreement; missing events;
conflicting contents; boundary disagreement; duplicate and ordering invariance;
malformed saved summaries; removed raw logs; same-provider refusal; and range
differences; fixed range selection across both live reads; and no agreement
output after a second-provider failure. The ancestor's 15 regression tests also passed. Mutated fixture
values in the tests are explicitly adversarial examples, never submitted as live
evidence.

A fresh attempt to read the older three-event demo range through PublicNode
returned HTTP 403 and controlled exit 2. No comparison JSON was emitted. This
provider access limit does not turn the retained real observations into invented
events, and does not imply the historical range has zero transfers.

The accompanying wall mark is **Twin Witness Trails**: Two ochre trails share a
chalk loop as Pepe checks one window with two witnesses. Image dimensions,
format, preservation checks and visual limitations are recorded in
`line-4/round-23-image-review.json` and `line-4/ROUND-23.md`.

## Schema 3 repair (round 27)

The validator accepts the producer's current schema 3 and retained schema 2.
An optional schema 3 `address_window_summary` is recomputed from validated raw
logs, including exact integer/string types, normalized address, and all flow
fields. A summary in schema 2, malformed summary, or unknown schema is rejected.
The receipt companion inherits this repair through its validator import.

On 2026-10-12 UTC, a fresh PublicNode ZTO capture at blocks 26179026–26179037
(schema 3, with the public ZTO contract address selected) passed crosscheck
validation and receipt creation. dRPC agreed on its zero transfers and boundary
anchors. The saved `round-27-live-zto.json` can be replayed without a network:

```sh
python3 -B line-4/tools/transfer-window-receipt/receipt.py --capture line-4/tools/transfer-crosscheck/round-27-live-zto.json
```

All 39 line tests passed (19 reader, 15 crosscheck, 5 receipt). New regressions
run the actual producer against dated real replies, feed its emitted schema 3
into both companions, retain schema 2 compatibility, and reject tampered address
summaries. Mocked transport tests are explicitly offline simulations. The older
historical live range returned HTTP 403; this failure was not treated as empty
evidence. Public-provider agreement and receipts remain observations, not
proofs of completeness, honesty, finality, or balances.

## Exact transfer event types (2026-10-13)

Saved transfer summaries now require the same JSON types as the events rebuilt
from raw logs. Previously Python equality could accept a boolean or float in an
integer field: for example, `true` in place of `1`, or `238.0` in place of `238`.
The validator now checks the list, each event object, its exact keys, and each
scalar's type and value. The fixed event shape needs no recursive traversal of
untrusted payloads. Receipt and other companions importing `checked()` inherit
the stricter check. Correct schema 2 and schema 3 captures remain compatible.

Tried offline on 2026-10-13:

```sh
python3 -B line-4/tools/transfer-crosscheck/test_crosscheck.py
```

All **21 tests passed**. Before the repair, the added regressions reproduced
nine accepted malformed summaries: equal floats for all three integer event
fields (`block`, `log_index`, `transaction_index`) and booleans replacing both
zero and one in each field. The suite also rejects altered strings, nested
containers, missing or extra event fields, invalid collection shapes, and
changed event counts or order. It accepts reordered object keys, the retained
real schema 2/3 captures, and captures emitted by the current producer with
retained real RPC replies. The low-block/index cases are deliberately mutated
test data, not claims about chain activity.

The offline `--demo` command above still returned **agreement** for the three
retained real ZTO transfers in blocks **26177298–26177309**, with exit code 0.
These checks do not establish provider completeness, independence, finality,
or any account balance.

A fresh dRPC observation at **2026-10-13T02:25:55Z** also returned those three
historical ZTO transfers and passed the repaired validator. Its schema 3 events,
boundary anchors and semantic receipt agree with the retained schema 2
PublicNode observation from 2026-10-12. This is one fresh read compared with
dated evidence, not two fresh concurrent observations. The original capture
is retained in `round-32-live-drpc.json`; replay it offline with:

```sh
python3 -B line-4/tools/transfer-window-receipt/receipt.py --capture line-4/tools/transfer-crosscheck/round-32-live-drpc.json
```

All six native Line 4 suites passed **65 tests** after the repair. A separate
scratch integration matrix rejected 395 malformed-event cases across the
validator and its four report consumers. Check summaries are in
`line-4/round-32-tests.json`, `line-4/round-32-integration-check.json` and
`line-4/round-32-live-check.json`. The companion mark **The Fitted Stones** shows
two notched ochre stones comparing their shapes beside Pepe; image dimensions,
format and visual limitations are recorded in `line-4/ROUND-32.md`.
