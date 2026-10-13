"""Behavioral checks for canonical JSON-to-RLP export."""

import contextlib
import io
import json
import unittest
from unittest.mock import patch

import envelope


class EnvelopeTests(unittest.TestCase):
    def test_minimal_canonical_vector(self):
        obj = envelope.rpc_reader.demo_object()
        for name in envelope.rpc_reader.QUANTITIES:
            obj[name] = "0x0"
        obj.update(to=None, data="0x", accessList=[])
        report = envelope.export(json.dumps(obj))
        self.assertEqual(report["unsignedEnvelopeHex"], "0x02c98080808080808080c0")
        self.assertEqual(report["byteLength"], 11)
        self.assertEqual(report["fieldSpans"][0],
                         {"field": "chainId", "startByte": 2, "endByteExclusive": 3})
        self.assertEqual(report["fieldSpans"][-1]["endByteExclusive"], 11)

    def test_demo_matches_inherited_bytes_and_inspection(self):
        report = envelope.export(json.dumps(envelope.rpc_reader.demo_object()))
        self.assertEqual(report["unsignedEnvelopeHex"], envelope.D.demo_transaction())
        self.assertEqual(report["inspection"]["destinationLabel"], "ZTO")
        self.assertEqual(report["inspection"]["transaction"],
                         envelope.rpc_reader.intent.interpret(report["unsignedEnvelopeHex"])["transaction"])
        raw = bytes.fromhex(report["unsignedEnvelopeHex"][2:])
        for span in report["fieldSpans"]:
            self.assertGreater(span["endByteExclusive"], span["startByte"])
            self.assertTrue(raw[span["startByte"]:span["endByteExclusive"]])

    def test_long_payload_creation_duplicates_and_input_alias(self):
        obj = envelope.rpc_reader.demo_object()
        obj["to"] = None
        obj["input"] = "0x" + "ab" * 60
        del obj["data"]
        obj["accessList"] = [{"address": envelope.D.ZTO,
                              "storageKeys": ["0x" + "12" * 32] * 2}] * 2
        report = envelope.export(json.dumps(obj))
        self.assertEqual(report["calldataSourceField"], "input")
        decoded = envelope.D.decode(report["unsignedEnvelopeHex"])
        self.assertIsNone(decoded["to"])
        self.assertEqual(decoded["data"], obj["input"])
        self.assertEqual(decoded["accessList"], obj["accessList"])
        self.assertEqual(bytes.fromhex(report["unsignedEnvelopeHex"][2:])[1], 0xf9)

    def test_uint256_and_field_boundaries(self):
        obj = envelope.rpc_reader.demo_object()
        obj["value"] = hex(2**256 - 1)
        report = envelope.export(json.dumps(obj))
        self.assertEqual(envelope.D.decode(report["unsignedEnvelopeHex"])["value"], 2**256 - 1)
        spans = report["fieldSpans"]
        self.assertEqual([item["field"] for item in spans], list(envelope.FIELD_NAMES))
        self.assertEqual([item["endByteExclusive"] for item in spans[:-1]],
                         [item["startByte"] for item in spans[1:]])

    def test_invalid_and_signed_json_rejected_without_output(self):
        for change in ({"r": "0x0"}, {"nonce": "0x00"}, {"data": "0x0"},
                       {"type": "0x1"}):
            obj = envelope.rpc_reader.demo_object()
            obj.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                envelope.export(json.dumps(obj))
        with self.assertRaises(ValueError):
            envelope.export('{"nonce":"0x0","nonce":"0x1"}')
        with patch("sys.stdin", io.StringIO("{")), \
                contextlib.redirect_stdout(io.StringIO()) as output, \
                contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(envelope.main(["--stdin"]), 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("error:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
