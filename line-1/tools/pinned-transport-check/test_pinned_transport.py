"""Offline checks for complete pinned transport and early rejection."""
import copy
import json
from pathlib import Path
import unittest
import pinned_transport_check as tool


class Tests(unittest.TestCase):
    def test_complete_transport_replay(self):
        result = tool.run_check()
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['checks_passed'], 68)
        self.assertFalse(result['network_used'])

    def test_forbidden_requests_never_reach_wire(self):
        for method, params, endpoint in [
            ('eth_sendRawTransaction', [], tool.pinned.rpc.DEFAULT_RPC),
            ('eth_chainId', [], 'http://example.com/rpc/1'),
            ('eth_call', [{}, 'latest'], tool.pinned.rpc.DEFAULT_RPC),
        ]:
            replay = tool.Sequence([None])
            with tool.wire.offline_wire(replay), self.assertRaises(ValueError):
                tool.pinned.public_read(endpoint, method, params)
            self.assertEqual(replay.requests, [])

    def test_reorg_rejected_through_actual_wire(self):
        retained = json.loads(Path(tool.HERE / 'example-zto.json').read_text())
        before = copy.deepcopy(retained['block'])
        after = copy.deepcopy(retained['block_after'])
        after['hash'] = before['parentHash']
        replay = tool.Sequence([retained['chain_id'], before, retained['result'], after])
        with tool.wire.offline_wire(replay), self.assertRaisesRegex(ValueError, 'hash changed'):
            tool.pinned.capture()
        self.assertEqual(len(replay.requests), 4)

    def test_wrong_chain_stops_wire_sequence(self):
        replay = tool.Sequence(['0x2'])
        with tool.wire.offline_wire(replay), self.assertRaisesRegex(ValueError, 'mainnet'):
            tool.pinned.capture()
        self.assertEqual(len(replay.requests), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
