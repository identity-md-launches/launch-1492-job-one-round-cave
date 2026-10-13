#!/usr/bin/env python3
"""Replay the pinned ZTO reader's complete HTTP pipeline without networking."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def sibling(name, file):
    spec = importlib.util.spec_from_file_location('pinned_check_' + name.replace('-', '_'),
                                                 HERE.parent / name / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pinned = sibling('pinned-snapshot', 'pinned_snapshot.py')
wire = sibling('transport-check', 'transport_check.py')


class Sequence(wire.Replay):
    """Feed four saved results through real urllib HTTP status handlers."""
    def __init__(self, values, failure=None):
        super().__init__(b'')
        self.values = values
        self.failure = failure

    def https_open(self, request):
        index = len(self.requests)
        if index >= len(self.values):
            raise AssertionError('unexpected extra request')
        self.raw = json.dumps({'jsonrpc': '2.0', 'id': 1,
                               'result': self.values[index]}).encode()
        self.status, self.headers = 200, {}
        if self.failure and index == self.failure[0]:
            self.raw, self.status, self.headers = self.failure[1:]
        return super().https_open(request)

    http_open = https_open


def run_check():
    source = (HERE / 'example-zto.json').read_bytes()
    retained = pinned.rpc.strict_json(source)
    pinned.inspect(retained)
    values = [retained['chain_id'], retained['block'], retained['result'],
              retained['block_after']]
    number = retained['block']['number']
    expected = [('eth_chainId', []),
                ('eth_getBlockByNumber', [retained['requested_block'], False]),
                ('eth_call', [pinned.CALL, number]),
                ('eth_getBlockByNumber', [number, False])]
    checks = []
    for endpoint, name in [(pinned.rpc.DEFAULT_RPC, 'https'),
                            ('http://127.0.0.1:1/rpc/1', 'loopback-wire-replay')]:
        replay = Sequence(values)
        with wire.offline_wire(replay):
            captured = pinned.capture(endpoint, retained['requested_block'])
        if pinned.inspect(captured) != pinned.inspect(retained):
            raise AssertionError('observation changed')
        requests = [pinned.rpc.strict_json(req.data) for req in replay.requests]
        if [(r['method'], r['params']) for r in requests] != expected:
            raise AssertionError('read order or explicit block pin changed')
        if any(req.get_header('User-agent') != pinned.rpc.USER_AGENT or
               req.get_header('Accept-encoding') != 'identity' for req in replay.requests):
            raise AssertionError('missing transport headers')
        checks.append(name + '-four-reads-no-proxies-no-sockets')
    failures = [
        ('redirect-' + str(status), b'', status,
         {'Location': 'https://eth.drpc.org'}) for status in (301, 302, 303, 307, 308)]
    failures += [
        ('http-error', b'private diagnostic', 503, {}),
        ('unexpected-http-success', b'{}', 201, {}),
        ('compressed', b'{}', 200, {'Content-Encoding': 'gzip'}),
        ('duplicate-key', b'{"jsonrpc":"2.0","id":1,"result":0,"result":1}', 200, {}),
        ('boolean-id', b'{"jsonrpc":"2.0","id":true,"result":null}', 200, {}),
        ('wrong-id', b'{"jsonrpc":"2.0","id":2,"result":null}', 200, {}),
        ('nonfinite', b'{"jsonrpc":"2.0","id":1,"result":NaN}', 200, {}),
        ('overflow', b'{"jsonrpc":"2.0","id":1,"result":1e400}', 200, {}),
        ('extra-field', b'{"jsonrpc":"2.0","id":1,"result":null,"extra":0}', 200, {}),
        ('provider-error', b'{"jsonrpc":"2.0","id":1,"error":{"code":-1,"message":"private"}}', 200, {}),
        ('oversize', b' ' * (pinned.LIMIT + 1), 200, {}),
    ]
    for stage in range(4):
        for name, raw, status, headers in failures:
            replay = Sequence(values, (stage, raw, status, headers))
            with wire.offline_wire(replay):
                try:
                    pinned.capture(tag=retained['requested_block'])
                except (ValueError, RuntimeError, OSError):
                    pass
                else:
                    raise AssertionError(name + ' accepted')
            if len(replay.requests) != stage + 1:
                raise AssertionError('read continued after failure')
            checks.append('stage-' + str(stage + 1) + '-' + name)
    # Real CLI failure path: do not leak diagnostics or output a partial snapshot.
    from unittest.mock import patch
    replay = Sequence(values, (2, b'private diagnostic', 503, {}))
    out, err = io.StringIO(), io.StringIO()
    with wire.offline_wire(replay), patch.object(sys, 'argv', ['pinned', 'capture']), \
         contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = pinned.main()
    if code != 1 or out.getvalue() or 'private' in err.getvalue():
        raise AssertionError('CLI leaked a partial result or diagnostic')
    checks.append('cli-failure-no-partial-evidence')
    for raw in (b'{"schema":0,"schema":1}', b'{"x":NaN}', b'{"x":1e400}'):
        stdin = io.TextIOWrapper(io.BytesIO(raw))
        with wire.offline_wire(Sequence(values)), patch.object(sys, 'argv', ['pinned', 'inspect']), \
             patch.object(sys, 'stdin', stdin), contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            if pinned.main() != 1:
                raise AssertionError('ambiguous offline JSON accepted')
    checks.append('offline-strict-json')
    return {'schema': 'pinned-transport-check/1', 'status': 'passed',
            'network_used': False, 'checks_passed': len(checks), 'checks': checks,
            'retained_evidence': {'sha256': hashlib.sha256(source).hexdigest(),
                                  'captured_at': retained['captured_at'],
                                  **pinned.inspect(retained)},
            'limits': 'Offline transport replay is not a new chain observation or provider authentication.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['demo'])
    parser.parse_args()
    try:
        print(json.dumps(run_check(), indent=2, sort_keys=True))
        return 0
    except (AssertionError, ValueError, RuntimeError, OSError, KeyError, TypeError):
        print('pinned-transport-check: regression or invalid retained evidence', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
