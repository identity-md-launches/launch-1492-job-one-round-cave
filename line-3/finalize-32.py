"""Add one image-tool pigment mark without changing ancestral wall pixels elsewhere.

Reads the generated PNG as base64 on stdin; never saves the cutout as a picture.
The final wall and its mandated thumbnail are the only images it writes.
"""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("prior_finalize", ROOT / "line-3/finalize-31.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
thumbnail = prior.thumbnail


def main():
    old_path = ROOT / "artifacts/line-3/wall.png"
    inherited = old_path.read_bytes()
    old_hash = hashlib.sha256(inherited).hexdigest()
    older = json.loads((ROOT / "dist/line-3/31.json").read_text())
    if older["image"] != "https://api.imd.fun/artifacts/" + old_hash:
        raise ValueError("the inherited wall does not match record 31")
    width, height, base_rows = thumbnail.png_rgb(inherited)
    if (width, height) != (1254, 1254):
        raise ValueError("unexpected inherited wall size")
    encoded = sys.stdin.buffer.readline(12_000_001).strip()
    if len(encoded) > 12_000_000:
        raise ValueError("image-tool cutout exceeds limit")
    cutout = base64.b64decode(encoded, validate=True)
    source_width, source_height, source = prior.png_rgba(cutout)

    # Right-side open rock, clear of every inherited painted figure and object.
    box = (1025, 355, 1205, 535)
    x0, y0, x1, y1 = box
    target_width, target_height = x1 - x0, y1 - y0
    rows = [bytearray(row) for row in base_rows]
    changed = 0
    for dy in range(target_height):
        sy0, sy1 = dy * source_height // target_height, (dy + 1) * source_height // target_height
        for dx in range(target_width):
            sx0, sx1 = dx * source_width // target_width, (dx + 1) * source_width // target_width
            red = green = blue = alpha = 0
            count = (sy1 - sy0) * (sx1 - sx0)
            for sy in range(sy0, sy1):
                scanline = source[sy]
                for sx in range(sx0, sx1):
                    r, g, b, a = scanline[4 * sx:4 * sx + 4]
                    alpha += a
                    red += r * a
                    green += g * a
                    blue += b * a
            if alpha == 0:
                continue
            opacity = min(210, alpha // count * 4 // 5)
            if opacity < 10:
                continue
            pigment = (red // alpha, green // alpha, blue // alpha)
            at = 3 * (x0 + dx)
            previous = rows[y0 + dy][at:at + 3]
            newer = bytes((previous[c] * (255 - opacity) + pigment[c] * opacity + 127) // 255
                          for c in range(3))
            if newer != previous:
                rows[y0 + dy][at:at + 3] = newer
                changed += 1
    if changed < 1000:
        raise ValueError("mark too faint or missing")
    outside = sum(rows[y][3 * x:3 * x + 3] != base_rows[y][3 * x:3 * x + 3]
                  for y in range(height) for x in range(width)
                  if not (x0 <= x < x1 and y0 <= y < y1))
    if outside:
        raise ValueError("ancestral pixels changed outside the mark")
    png = prior.encode_rgb(width, height, rows)
    if thumbnail.png_rgb(png)[2] != [bytes(row) for row in rows]:
        raise ValueError("saved PNG did not decode identically")
    jpg = thumbnail.jpeg(thumbnail.resize(width, height, rows))
    if len(jpg) >= 100_000:
        raise ValueError("JPEG exceeds 100 KB limit")
    digest = hashlib.sha256(png).hexdigest()
    meaning = "Pepe packs loose pieces into one tied bundle whose shape can be checked."
    record = {
        "name": "The Tied Bundle",
        "image": "https://api.imd.fun/artifacts/" + digest,
        "attributes": [{"trait_type": key, "value": value} for key, value in [
            ("Cave", "Base"), ("Wall", "Line 3"), ("Number", 32),
            ("Left behind", "canonical-envelope"), ("Meaning", meaning),
            ("One thing", "Offline EIP-1559 transaction decoding")]],
    }
    (ROOT / "artifacts/line-3/wall-v13.png").write_bytes(png)
    old_path.write_bytes(png)
    (ROOT / "dist/line-3/32.jpg").write_bytes(jpg)
    (ROOT / "dist/line-3/32.json").write_text(json.dumps(record, indent=2) + "\n")
    review = {
        "wall": {"paths": ["artifacts/line-3/wall-v13.png", "artifacts/line-3/wall.png"],
                 "width": width, "height": height, "format": "PNG", "mode": "RGB",
                 "bytes": len(png), "sha256": digest},
        "thumbnail": {"path": "dist/line-3/32.jpg", "width": 512, "height": 512,
                      "format": "JPEG", "bytes": len(jpg)},
        "preservation": {"inheritedSha256": old_hash, "editRectangleXYXY": list(box),
                         "changedPixels": changed, "changedPixelsOutsideRectangle": outside},
        "cutout": {"width": source_width, "height": source_height, "format": "PNG", "mode": "RGBA"},
        "visualReview": {"reviewed": False},
        "unmetVisualRequirements": ["Visual review pending"],
    }
    (ROOT / "line-3/round-32-review.json").write_text(json.dumps(review, indent=2) + "\n")
    print(json.dumps(review, indent=2))


if __name__ == "__main__":
    main()
