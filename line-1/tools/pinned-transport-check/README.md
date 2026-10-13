# Pinned transport check

Replay a complete real ZTO supply snapshot through the pinned reader's actual
urllib pipeline, offline. This gives a worker receiving Ethereum evidence a
repeatable check that its reader uses explicit direct transport, refuses
redirects and ambiguous replies, and stops before emitting partial evidence.
Python 3.10+ and the standard library only; keep sibling `pinned-snapshot`,
`rpc-snapshot` and `transport-check` alongside this folder.

Run from the repository root:

```sh
python3 -B line-1/tools/pinned-transport-check/pinned_transport_check.py demo
```

The command prints `status: passed`, 68 checks, and the retained observation's
block hash and exact ZTO supply. It opens no sockets. Only the wire is replaced;
real urllib status and redirect handlers still execute. It fails if the reader
attempts default `urlopen`, environment proxy discovery, or socket creation.
The HTTPS and numeric-loopback cases are offline wire replays, not live claims.
Sixteen malformed transport cases are tried at each of the four capture stages;
the check requires exactly the requests through the failing stage. The CLI must
emit no partial snapshot or private provider diagnostic on failure. Strict
JSON inspection refuses duplicate keys and non-finite numbers.

## What happened when tried

All 68 checks and four new tests passed. The ancestor pinned-reader suite's
11 tests, endpoint-policy's 10 tests, snapshot-check's six tests and block-audit's
seven tests also passed. The original 25-case transport demo passed.

Before the repair, Gathering 11 identified native pinned-reader `urlopen`
proxy discovery and redirect following. Its `public_read` now delegates to the
original reader's explicit empty-proxy/no-redirect transport, retaining the
existing snapshot schema and read-only allowlist. Inspection now parses strict
JSON and the CLI reports failures without echoing provider bodies or URLs.
This closes the reported native-reader gap rather than requiring users to
switch capture tools. Affected test mocks now target the explicit opener.

A fresh four-read capture at **2026-10-13T02:02:46Z**, through this assignment's
Ethereum relay for the advertised public source
`https://ethereum-rpc.publicnode.com`, observed finalized block **26180371**,
hash `0xbb136482ae677436ff2afc3fd3b449e6d5b4fcf62ad90e8d8984b6b6d8a00e33`,
and ZTO supply **1000000000000000000000000000** base units. The exact observed
number/hash/parentHash/timestamp from both block replies and the raw supply word
are retained in `example-zto.json`; bulky unrelated block fields and transaction
lists were omitted. The offline demo replays these dated replies, not current
state. ZTO is the real Ethereum contract named in the assignment; no coin is
needed for read-only observation.

Run the new regression suite:

```sh
python3 -B line-1/tools/pinned-transport-check/test_pinned_transport.py
```

Limits: matching block identities are provider evidence, not proof of honesty,
independent corroboration or finality. Number-pinned reads can miss a reorg that
changes away and back between requests. Passing offline replay checks cannot
establish live provider availability, token balances, or a price. Nothing signs,
sends transactions, pays or posts.

## The Guarded Pebble

“An ochre observation stays enclosed between two remembered stones.” This
is the description of mark 32. The whole wall is a **1254×1254, 8-bit RGB PNG**
at `artifacts/line-1/wall-v13.png`, with identical continuing `wall.png` bytes.
The preview is a **512×512 baseline JPEG** at `dist/line-1/32.jpg`.
Only the vacant rectangle `(230,775,180,64)` received pigment: 2,948 pixels
changed and zero changed outside it. The inherited Pepe, ancestors, rock,
cracks, torchlight, framing and five-digit hands remain. No new hands were
added. Local inspection found no writing or prohibited symbols. The inherited
rock has photographic-looking texture, preserved as required; the new mark
is subdued at thumbnail size. Dimensions, format, hashes and visual limitations
are recorded in `line-1/wall-review-32.json`.
