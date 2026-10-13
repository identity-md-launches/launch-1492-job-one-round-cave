#!/usr/bin/env python3
"""Check Gathering 12's output contract without network or image libraries."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'gathering/checks/round-12/deliverable.json'
PLACEHOLDER = {'name': 'Not painted yet',
               'image': 'https://api.imd.fun/artifacts/9cbb7bb2a41efa92e010921f287819c9ffb02c4375fa9496c8468701d8e00cc5',
               'attributes': [{'trait_type': 'Cave', 'value': 'Base'}]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section = None
        self.cards = {}
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'section':
            self.section = values['id']
            self.cards[self.section] = []
        elif tag == 'article':
            self.cards[self.section].append(int(values['data-number']))
        elif tag == 'script':
            self.scripts += 1


def main():
    wall = ROOT / 'artifacts/gathering/wall-v13.png'
    same = ROOT / 'artifacts/gathering/wall.png'
    preview = ROOT / 'dist/gathering/12.jpg'
    record = json.loads((ROOT / 'dist/gathering/12.json').read_text())
    assert set(record) == {'name', 'image', 'attributes'}
    assert [row['trait_type'] for row in record['attributes']] == [
        'Cave', 'Wall', 'Number', 'Left behind', 'Meaning', 'One thing']
    assert all(set(row) == {'trait_type', 'value'} for row in record['attributes'])
    assert [record['attributes'][i]['value'] for i in (0, 1, 2, 5)] == [
        'Base', 'Gathering', 12, 'Gathering']
    assert type(record['attributes'][2]['value']) is int
    assert record['image'] == 'https://api.imd.fun/artifacts/' + sha(wall)
    assert wall.read_bytes() == same.read_bytes()
    assert {p.name for p in (ROOT / 'artifacts/gathering').iterdir()} == {
        'wall-v13.png', 'wall.png'}
    data = wall.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR'
    width, height, depth, color, compression, filtering, interlace = struct.unpack_from(
        '>IIBBBBB', data, 16)
    assert (width, height, depth, color, compression, filtering, interlace) == (
        1254, 1254, 8, 2, 0, 0, 0)
    probe = subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,codec_name', '-of', 'json', str(preview)])
    info = json.loads(probe)['streams'][0]
    assert (info['width'], info['height'], info['codec_name']) == (512, 512, 'mjpeg')
    assert preview.stat().st_size < 100000
    review = json.loads((ROOT / 'gathering/checks/round-12/wall-review.json').read_text())
    assert review['changed_pixels'] > 0 and review['changed_pixels_outside_rectangle'] == 0
    assert review['unmet_visual_requirements'] == []

    goals = [{'line': n, 'goal': (ROOT / f'line-{n}/GOAL.md').read_text().strip()}
             for n in range(1, 5)]
    assert json.loads((ROOT / 'dist/goals.json').read_text()) == goals
    gallery = Gallery()
    page = (ROOT / 'dist/index.html').read_text()
    gallery.feed(page)
    assert gallery.scripts == 0 and len(page.encode()) < 100000
    count = 0
    for folder in ['line-1', 'line-2', 'line-3', 'line-4', 'gathering']:
        records = sorted((ROOT / 'dist' / folder).glob('[0-9][0-9].json'), reverse=True)
        painted, pending = [], []
        for path in records:
            item = json.loads(path.read_text())
            number = int(path.stem)
            if item['name'] == 'Not painted yet':
                assert item == PLACEHOLDER and not path.with_suffix('.jpg').exists()
                pending.append(number)
            else:
                assert path.with_suffix('.jpg').exists()
                painted.append(number)
        assert all((ROOT / 'dist' / folder / f'{n:02d}.json').exists()
                   for n in range(2, 22))
        assert gallery.cards[folder] == painted + pending
        count += len(records)
    assert count == 149

    provenance = json.loads((ROOT / 'shared/flow-handoff/PROVENANCE.json').read_text())
    for dependency in provenance['dependencies']:
        assert sha(ROOT / dependency['source']) == dependency['sha256'] == sha(ROOT / dependency['copy'])
    trial = provenance['round_12_trial']
    assert sha(ROOT / trial['source']) == trial['sha256'] == sha(ROOT / trial['copy'])
    assert sha(ROOT / trial['archive']) == trial['archive_sha256']
    changed = subprocess.check_output(['git', 'status', '--porcelain', '-z', '--untracked-files=all'], cwd=ROOT)
    paths = [entry[3:].decode() for entry in changed.split(b'\0') if entry]
    assert all(path.startswith(('gathering/', 'shared/', 'artifacts/gathering/', 'dist/')) for path in paths)
    assert not subprocess.check_output(['git', 'status', '--porcelain', '--', 'line-1', 'line-2', 'line-3', 'line-4'], cwd=ROOT)
    assert not subprocess.check_output(['git', 'ls-files', '--', 'artifacts/gathering'], cwd=ROOT)
    assert all(p.stat().st_size < 100000 for folder in ('gathering', 'shared', 'dist')
               for p in (ROOT / folder).rglob('*') if p.is_file())
    assert (ROOT / 'gathering/COINS.md').read_text().startswith('none\n')
    report = (ROOT / 'gathering/REPORT.md').read_text()
    assert all(f'## Line {n}' in report for n in range(1, 5))
    result = {'passed': True, 'record_number': 12, 'wall_dimensions': [width, height],
              'wall_format': '8-bit RGB PNG', 'wall_sha256': sha(wall),
              'preview_dimensions': [info['width'], info['height']],
              'preview_format': 'JPEG', 'preview_bytes': preview.stat().st_size,
              'changed_pixels_outside_rectangle': 0, 'unmet_visual_requirements': [],
              'gallery_records': count, 'gallery_bytes': len(page.encode()),
              'source_paths_in_scope': True, 'line_folders_unchanged': True,
              'shared_source_hashes_match': True}
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
