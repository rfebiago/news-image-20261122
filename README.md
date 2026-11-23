# news-image-20261122 — FINAL edition

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rfebiago/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rfebiago/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up Sunday 22 November 2026's world news in one image (make.fun,
$100, closes Tue 24 Nov 2026 07:00 WIB).

## Status

**FINAL.** The 23 Nov refresh is DONE and verified — this edition is
ready to submit. Built Mon 23 Nov 2026 ~10:00–11:00 WIB, then fixed in
a post-review round ~11:00–12:00 WIB (see REBUILD_NOTES.md).

Sunday's big results are all in as results, not fixtures: Liverpool
4–0 Man Utd (Pochettino debut, Yoro sent off 8') and Alcaraz beats
Zverev 6–2, 7–6(7) are promoted to heroes, alongside the COP31
collapse lead. The Cikande toll is updated to the Sunday-evening state
(3 confirmed dead, 24 body bags recovered, 34 missing), Nigeria's boat
toll 24 → 29, and all four former single-source items are now
second-sourced. The misdated Gaza Board of Peace line was cut and
replaced with Shuri Castle. See REBUILD_NOTES.md and SOURCES.md.

## Files

- `main.ts` — entrypoint (Node 22, stdlib only): copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (or `/output`).
- `draw_entry.py` — draws `entry.png` (1024×1024, PIL, no network).
  Edit ONLY its DATA tables for a refresh; it fails (exit 1) on any
  text overflow.
- `entry.png` — 1024×1024, 209,802 bytes, 40 stories
  (1 lead + 3 heroes + 16 smalls + 20 also-on), 7 regions.
  sha256 `915407a3dcba4c8e3ce80a9ccae77af4d47a5bf43560cce5947330f30e87d9d1`.
- `DESIGN_NOTES.md`, `SOURCES.md`, `REVIEW.md`, `REBUILD_NOTES.md`,
  `LICENSE` (MIT).

## Verify

```sh
python3 draw_entry.py            # twice -> identical sha256
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # twice -> identical
```

Verified this build: draw twice byte-identical, main.ts twice
byte-identical (output sha256
`915407a3dcba4c8e3ce80a9ccae77af4d47a5bf43560cce5947330f30e87d9d1`),
PNG whole 1024×1024 RGB, 209,802 bytes ≤ 1 MiB. Post-build review
in REVIEW.md (CONDITIONAL PASS, all findings fixed and re-verified).
