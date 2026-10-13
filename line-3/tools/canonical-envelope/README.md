# Canonical unsigned envelope

`envelope.py` turns a **complete unsigned EIP-1559 JSON transaction object** into
canonical type-2 RLP bytes. It reports the exact byte range of each of the nine
fields and includes the inherited offline transaction inspection. A worker can
compare the emitted bytes with an independently supplied envelope or inspect
which RLP bytes belong to a field. Byte ranges are zero-based, include each
field's RLP prefix, and end just before `endByteExclusive`.

From the repository root, one command shows it working:

```sh
python3 -B line-3/tools/canonical-envelope/envelope.py --demo
```

Tried locally: exit 0; the synthetic ZTO `totalSupply()` example produced a
46-byte envelope beginning `0x02ec`, with nine contiguous field spans. Its
full output round-tripped through the inherited decoder and was byte-identical
to that decoder's existing demonstration. ZTO's destination is the real Ethereum
contract `0xd782bdea4ef02a0bd391eb9089470c8080f0a68e`; nonce, fees, gas and
call are demonstration values, with no chain observation or execution claim.

Pass a complete JSON object as one quoted argument or with `--stdin`. The JSON
profile is the unchanged sibling `rpc-unsigned-reader` profile: all unsigned
fields required; exactly one of `data` or `input`; `to: null` for creation;
canonical bounded hex quantities; exact-length addresses and storage keys;
ordered access list with duplicates retained. Duplicate JSON keys, sender or
signature fields, missing fields, numeric JSON values, unsupported transaction
types and over-limit inputs are rejected. The inherited limits are 512 Ki
characters of JSON, 128 KiB of encoded bytes and 16,384 RLP items. Success exits
0; invalid input exits 2 with no partial JSON output.

The `sha256Fingerprint` identifies these **unsigned input bytes** for local
comparison. It is not an Ethereum transaction hash, signature or sender identity.
The exported bytes and the inspection cannot establish chain state, usable nonce,
balance, contract behavior, gas sufficiency, inclusion or safety. This tool does
not read files or environment variables, use a key or wallet, sign, send, pay or
post. It makes no network request. It uses Python 3.10+ standard library and the
committed sibling `rpc-unsigned-reader`, `erc20-intent` and
`zto-eip1559-decoder` modules; keep those folders together.

I also ran:

```sh
python3 -B -m unittest discover -s line-3/tools/canonical-envelope -v
```

All five behavioral tests passed. They cover a hand-checked minimal RLP vector,
byte-for-byte agreement with the inherited ZTO demo, long RLP payloads, creation,
ordered duplicate access-list entries, the `input` alias, uint256 boundaries,
contiguous spans and rejection of malformed or signed JSON. No dependency was
installed.

## Round 32 mark

**The Tied Bundle:** a small worn ochre pouch with a charcoal tie on open
right-side stone. The image tool supplied pigment only; the final compositor
kept every inherited pixel outside `(1025, 355, 1205, 535)` exactly unchanged.
`artifacts/line-3/wall-v13.png` and continuing `wall.png` are identical
1254×1254 RGB PNGs. `dist/line-3/32.jpg` is a 512×512 JPEG and `32.json` names
the whole wall's SHA-256. `line-3/round-32-review.json` records formats,
dimensions, the preserved area and visual review. The image and thumbnail were
inspected: inherited Pepe remains broad-mouthed and heavy-lidded, with four
fingers and an opposing thumb on each visible hand; no hand was added. No
letters, numbers, captions, logos, watermark, border, real people or prohibited
symbols were observed. The mark is intentionally small at thumbnail size.
