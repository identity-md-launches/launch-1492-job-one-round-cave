#!/usr/bin/env python3
"""Export canonical unsigned type-2 RLP from a complete JSON transaction."""

import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rpc-unsigned-reader"))
import rpc_reader


D = rpc_reader.D
FIELD_NAMES = ("chainId", "nonce", "maxPriorityFeePerGas", "maxFeePerGas",
               "gasLimit", "to", "value", "data", "accessList")


def _prefix(size, list_item):
    base = 0xc0 if list_item else 0x80
    if size < 56:
        return bytes((base + size,))
    length = size.to_bytes((size.bit_length() + 7) // 8, "big")
    return bytes((base + 55 + len(length),)) + length


def _bytes(value):
    if len(value) == 1 and value[0] < 0x80:
        return value
    return _prefix(len(value), False) + value


def _integer(value):
    return _bytes(b"" if value == 0 else value.to_bytes((value.bit_length() + 7) // 8, "big"))


def _list(parts):
    payload = b"".join(parts)
    return _prefix(len(payload), True) + payload


def export(json_text):
    """Validate a complete unsigned JSON object and return exact bytes and spans.

    The sibling reader enforces all field, size and ambiguity limits. This module
    serializes its decoded values independently and checks the complete result
    against the original inspection. No sender or chain state is supplied.
    """
    source = rpc_reader.inspect_json(json_text)
    tx = source["inspection"]["transaction"]
    access = []
    for entry in tx["accessList"]:
        slots = _list([_bytes(bytes.fromhex(slot[2:])) for slot in entry["storageKeys"]])
        access.append(_list([_bytes(bytes.fromhex(entry["address"][2:])), slots]))
    fields = [
        _integer(int(tx["chainId"])),
        _integer(int(tx["nonce"])),
        _integer(int(tx["maxPriorityFeePerGas"])),
        _integer(int(tx["maxFeePerGas"])),
        _integer(int(tx["gasLimit"])),
        _bytes(b"" if tx["to"] is None else bytes.fromhex(tx["to"][2:])),
        _integer(int(tx["value"])),
        _bytes(bytes.fromhex(tx["data"][2:])),
        _list(access),
    ]
    payload = b"".join(fields)
    header = b"\x02" + _prefix(len(payload), True)
    raw = header + payload
    if len(raw) > D.MAX_TRANSACTION_BYTES:
        raise ValueError("unsigned envelope exceeds the 128 KiB limit")
    encoded_hex = "0x" + raw.hex()
    if rpc_reader.intent.interpret(encoded_hex) != source["inspection"]:
        raise ValueError("encoded envelope did not round-trip to the inspected transaction")
    cursor = len(header)
    spans = []
    for name, field in zip(FIELD_NAMES, fields):
        spans.append({"field": name, "startByte": cursor, "endByteExclusive": cursor + len(field)})
        cursor += len(field)
    assert cursor == len(raw)
    return {
        "schema": "canonical-envelope/v1",
        "unsignedEnvelopeHex": encoded_hex,
        "byteLength": len(raw),
        "sha256Fingerprint": hashlib.sha256(raw).hexdigest(),
        "fieldSpans": spans,
        "calldataSourceField": source["calldataSourceField"],
        "inspection": source["inspection"],
    }


def main(args):
    try:
        if args == ["--demo"]:
            source = json.dumps(rpc_reader.demo_object())
        elif args == ["--stdin"]:
            source = sys.stdin.read(rpc_reader.MAX_JSON_CHARS + 1)
        elif len(args) == 1 and not args[0].startswith("--"):
            source = args[0]
        else:
            print("usage: envelope.py --demo | --stdin | 'JSON_OBJECT'", file=sys.stderr)
            return 2
        result = export(source)
    except (ValueError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
