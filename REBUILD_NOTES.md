# REBUILD_NOTES — news-image-20261122 (FINAL edition)

Status: FINAL edition built Mon 23 Nov 2026 ~10:00–11:00 WIB, then
FIXED in a post-review round ~11:00–12:00 WIB (see below).
**This edition IS final. The 23 Nov refresh is DONE — submit this
edition (parent handles bundling + check + submit).**

## Post-review fix round (Mon 23 Nov ~11:00–12:00 WIB)

The post-build review helper returned CONDITIONAL PASS with one P0
and three P1/P2 findings. All were fixed and re-verified before this
commit (entry.png sha256 changed 635558c1… → 915407a3…):

- **P0 Gaza misdate:** the Board of Peace report was delivered Tue
  17 Nov, not Sun 22 Nov (the Al Jazeera page timestamp was a
  republication). Line replaced with Shuri Castle (verified Sunday);
  DATE CHECK now names the Tue 17 Nov report as a trap; SOURCES.md's
  "page timestamp = event date" reasoning corrected.
- **P1 Cikande stale:** panel updated from the Sunday-morning
  snapshot (3/36/7 body bags) to the evening state (3 confirmed dead,
  24 body bags, 34 missing); numbers strip 36→34. SOURCES.md's false
  claim that "24" was unverifiable is retracted in the file.
- **P1 Florida wording:** "still near its record high" → "holds at a
  new all-time high" (river sits above the 1953 record).
- **P2 Manipur:** 18 → official 17 (228 in hospital); SOURCES.md
  explains the 17-vs-18 discrepancy.
- **P2 Smalls borders:** pitch fix + new vertical-extent guard (see
  "Known weaknesses" §7 below — the guard now enforces it).
- **P2 Strip label:** "STRØM 251.3 PTS" → "STRØM WINS" (no repeat).
- **Process:** REVIEW.md + this file rewritten for the final edition
  (the helper had read them before the rewrite landed).

## What the refresh fixed vs the late-Sunday edition

- Liverpool–Man Utd and the ATP final are now RESULTS, not fixtures:
  Liverpool 4–0 (Pochettino debut, Yoro sent off 8') and Alcaraz beats
  Zverev 6–2, 7–6(7) (maiden title, three set points saved) — both
  promoted to heroes.
- Cikande toll updated to the Sunday-evening state: 3 confirmed dead,
  24 body bags recovered, 34 missing (Reuters/AP/Xinhua/detikNews).
  Body bags are never printed as a death toll. (An earlier draft of
  this file wrongly claimed the "24" was unverifiable; that claim was
  retracted in the post-review round — see above.)
- Nigeria boat toll 24 → 29 (Gov Diri, Sunday; Tinubu ₦250m aid).
- Four single-source items all second-sourced: Manipur (official toll
  17 Sun, 228 in hospital), Korea minister (Reuters + JoongAng +
  Guardian), Florida flood (record broke Thu 19 Nov; river holds at a
  new all-time high Sun), Houthi (Reuters + TBS + Al Jazeera).
- New stories: Hull 2–0 Brighton (small), Delta system failure
  (small), Korea minister quits (small), AFCON 2027 host cities
  (also-on), Shuri Castle (also-on — restored in the post-review round
  as the replacement for the misdated Gaza line).
- Bolsonaro updated: stable in ICU, day 2, surgery not ruled out.
- "LATE-SUNDAY EDITION" eyebrow → "FINAL EDITION"; footer build line
  rewritten; DATE CHECK rewritten (Monday IND–NZ trap + Thu St Johns
  record added, TONIGHT clause removed).
- Kicker + numbers strip are now all Sunday figures (4–0, 720/9, 352,
  5–0, 3–2, 251.3, 34, 14).
- Helper rounds held this session (QUALITY / HELPERS-MAX rules):
  design discussion before the rebuild + post-build review after —
  see REVIEW.md §5–6. Helpers delivered analysis only; all entry
  text/code authored by the implementation builder in its own session.

## Known weaknesses of this edition

1. **Oceania 0.** No Oceania story: the Australia T20 was cut and the
   India Test is counted by team (Asia), not venue (Wellington).
   A future daily entry should keep one Oceania line if a verified
   result exists.
2. **Hero bodies are terse.** The 2-line discipline forced cuts
   (Liverpool drops the scorer list; Alcaraz drops the $5.17m prize).
   If a future layout grows a hero box, keep the overflow guard green.
3. **Manipur toll is a moving figure.** Official progression 11 Fri →
   16 Sat → 17 Sun; one outlet reports 18 (different Chandel count).
   Methanol is still only suspected (no lab confirmation). The image
   uses the official 17; a later rebuild would need a fresh check, not
   a carry-over.
4. **Cikande toll will move again.** 3 confirmed dead / 24 body bags /
   34 missing is the end-of-Sunday state, but DNA identification will
   take 2–3 weeks and floors were still being cleared. Any later edition
   must re-check rather than carry these numbers forward.
5. **Smalls pitch is tight by design.** The post-review pitch fix
   (headline 13 px, body 11 px) leaves ~2 px of slack in the fullest
   panels. A future rebuild that lengthens a small body must watch the
   new vertical-extent guard — it will fail the build rather than let
   text cross a border.
6. **Smalls are texture at 300 px.** Same as every dense broadsheet
   in this series; headlines carry the stories at small size, bodies
   are full-size bonus detail. The masthead, kicker, strip, lead and
   heroes are all legible at 300 px.

## How to rebuild (for a future competition of the same kind)

Edit ONLY the DATA tables in `draw_entry.py` (LEAD, HEROES, SMALLS,
ALSO_ON, NUMBERS, DATE_CHECK, EYEBROW_R, BUILD_LINE) and re-run
`python3 draw_entry.py`. The layout code does not change — except for
the one genuine fix this round: the smalls pitch (headline 13 px, body
11 px, start y+16) + the vertical-extent guard, added because the old
guard checked line counts only and let descenders cross panel borders.
The script fails (exit 1) on any text overflow — fix the copy, never
silence the guard. Keep commits granular: one commit per refresh round
(data + entry.png + docs).

## Top-3 lesson applied (and to keep applying)

Winners are dense (34–48 stories), name the date huge, lead with
numbers, and are fully self-contained (the judge has no news feed).
This edition follows that shape at 40 stories with 3-of-3 Sunday
heroes and an all-Sunday kicker + numbers strip. Do not copy any
entrant's wording or layout beyond these generic conventions.

## Refresh checklist — all items closed

1. Liverpool–Man Utd result ✓ (4–0, hero). Hull–Brighton ✓ (2–0, small).
2. ATP final winner ✓ (Alcaraz, hero).
3. Candy-factory toll update ✓ (panel + numbers strip together).
4. Second-source or drop: Manipur ✓, Korea minister ✓, Florida flood ✓,
   Houthi ✓ — all four second-sourced and kept.
5. Sunday-evening / Monday-early breaking news ✓ (Delta failure; no
   other dominant US Sunday story found).
6. Bolsonaro update ✓ (stable day 2); Gaza claims update ✓ (Board of
   Peace report is Tue 17 Nov — NOT Sunday, line cut, DATE CHECK names
   it as a trap; strike claims NOT used — unverified); IND–NZ day 5
   (Mon) NOT presented as Sunday news ✓ (DATE CHECK names the trap).
7. Africa item ✓ (AFCON 2027 host cities — Africa now 2 stories).
8. Re-verified every date tag; re-counted stories (40); re-ran
   determinism (draw script twice, main.ts twice) and the 300 px
   legibility check; updated SOURCES.md ✓.
9. Removed the footer "final refresh still mandatory" wording ✓.
