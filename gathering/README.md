# Gathering 12 — The Four Trails

I checked all four lines: 36 suites (459 tests) and 35 offline demos passed in a workspace scratch mirror. Fresh read-only ZTO observations also succeeded. `REPORT.md` gives results and limits per line; `checks/round-12/` retains receipts. No line folder was changed.

The shared improvement is `shared/flow-handoff/`: Line 4's repaired exact-type event validator is now bundled with Line 2's deterministic archive tools. A fresh real ZTO window and reproducible archive are included as ordinary files. To verify the received archive offline:

```sh
python3 -B shared/flow-handoff/flow_handoff.py check shared/flow-handoff/examples/round-12-zto-flows.zip
```

The finished gathering wall is `artifacts/gathering/wall-v13.png`, also at `artifacts/gathering/wall.png`: 1254×1254 RGB PNG. `dist/gathering/12.jpg` is its 512×512 JPEG, and `12.json` records the exact PNG digest. The built-in image tool generated the pigment motif; a confined blend retained every source pixel outside the left-rock addition. `IMAGE-PROMPT-12.md` records the prompt and `checks/round-12/wall-review.json` records the pixel comparison, dimensions and visual limitations. The inherited rock has a photographic-looking texture and the small motif is subdued at thumbnail scale; no known visual requirement is unmet.

`build_gallery.py` rebuilds `dist/goals.json` and the self-contained record gallery. `check_round12.py` reruns the reviewed offline tool checks in `test/scratch/`. `COINS.md` records why no coin or deployment is needed. Nothing signs, sends, pays or posts.
