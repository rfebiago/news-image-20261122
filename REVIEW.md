# REVIEW — news-image-20261122 FINAL edition (builder + helper review)

- **Reviewer:** the implementation builder, in-session, Mon 23 Nov
  2026 ~10:00–12:00 WIB, with a design-discussion helper round before
  the rebuild (§5) and a post-build review helper round after it (§6).
- **Reviewed:** `draw_entry.py`, `main.ts`, `entry.png` (full size +
  300×300 downscale + 2× crop of the smalls grid), `README.md`,
  `DESIGN_NOTES.md`, `SOURCES.md`, `REBUILD_NOTES.md`.
- **Verdict: FINAL PASS.** Gate clean, facts verified (see §3), the
  post-review helper's P0/P1 findings fixed and re-verified (§6).
  The 23 Nov refresh is DONE — this edition is ready for the parent
  to bundle + check + submit. Do NOT rebuild again without a fresh
  reason: the competition closes Tue 24 Nov 07:00 WIB.

## 1. GATE — all checks re-run fresh this run, all pass

| Check | Result |
|---|---|
| `draw_entry.py` run twice | Byte-identical; sha256 `915407a3dcba4c8e3ce80a9ccae77af4d47a5bf43560cce5947330f30e87d9d1`; exit 0, zero overflow errors |
| `main.ts` run twice (`MAKEFUN_OUTPUT_DIR=/tmp/out1`, `/tmp/out2`, Node v24.22.1) | Byte-identical; `cmp` clean vs committed `entry.png`; same sha256 |
| PNG whole | PIL loads cleanly: 1024×1024, RGB, PNG |
| Size | 209,802 bytes ≤ 1 MiB (1,048,576) ✓ |
| Story count | 1 lead + 3 heroes + 16 smalls + 20 also-on = **40** ✓ (eyebrow says 40) |
| Regions | EUROPE 13 · ASIA 9 · MIDDLE EAST 4 · N. AMERICA 7 · AFRICA 2 · S. AMERICA 1 · GLOBAL 4 = 40 ✓ (per-story assignments listed in SOURCES.md) |
| Kit local grade/check command | None — server-side grading only (RULES.txt grades on the server; the only local check is the pre-submit `node cli/makefun.mjs check`, a submission-time step) |

## 2. DEFECTS FOUND BY THE OVERFLOW GUARD + VISUAL REVIEW (all fixed)

- **D1 — numbers-strip label too wide.** First render of the final
  data: "LIVERPOOL BEAT MAN UTD" overflowed its cell. Fix: label
  shortened to "BEAT MAN UTD" in copy, never by silencing the guard.
- **D2 — smalls bodies crossed panel borders (found by the post-build
  review helper, §6).** The old guard checked line counts only; a
  2-line headline + 3-line body ends ~3 px past the 78 px panel box,
  and descenders sat on the bottom border in ~5 panels. Fix: layout
  genuinely had to change — headline pitch 14→13 px, body pitch
  12→11 px, headline start y+17→y+16, PLUS a new vertical-extent
  guard that fails the build if any small's text ends past its box.
  Verified fixed with a 2× crop of the whole smalls grid: no
  descender crosses any border.
- **D3 — numbers-strip label repeated the numeral.** "STRØM 251.3 PTS"
  under a big "251.3". Fix: label changed to "STRØM WINS".
- **Visual check (full size):** no overlaps, no truncated text, no
  garbled glyphs. ₦ renders ("Tinubu gives ₦250m aid"), Ø renders
  ("STRØM"), en-dashes render throughout. DATE CHECK fits in 2 lines
  inside its red box; footer ends inside the page.
- **300 px downscale:** masthead date, numbers strip, lead headline
  and all hero headlines remain legible. Small panels are texture at
  that size (expected for a dense broadsheet; same as the 21 Nov
  final). DATE CHECK footer is fine print by design.

## 3. DATE + FACT SPOT-CHECKS (fresh searches this run)

- COP31 collapse Sun 22 Nov — CNN + UN News + WRI, all dated 22 Nov. ✓
- India 720/9 dec, NZ 119/2, trail 233 — Reuters + SuperSport + Cricbuzz. ✓
- Liverpool 4–0 Man Utd — Reuters + Sky: Yoro sent off 8', Szoboszlai
  10', Wirtz 13', Ngumoha 66', Muñoz 82'; United 19th, 1 win in 11. ✓
- Alcaraz beats Zverev 6–2, 7–6(7) — Reuters + ATP Tour: maiden title,
  three set points saved, third Spaniard (Orantes 1976, Corretja 1998),
  5–0 through the tournament. ✓ (One ATP page snippet carries a "7–6(6)"
  typo in headline metadata; 7–6(7) is correct — tie-break 9–7.)
- Barça 3–2 Villarreal, from 0–2 down — Reuters 22 Nov. ✓
- Hull 2–0 Brighton — Reuters: McBurnie stoppage-time brace, Costinha
  sent off, Hull's first win since August. ✓
- HK Open finals: Wang 21–16, 21–11 vs Pornpawee; Antonsen walkover —
  Wikipedia + Flashscore + Straits Times. ✓
- Strøm 251.3, Kvandal 240.4, Hansen 239.1 — FIS 22 Nov. ✓
- Nigeria boat: capsized Fri, toll 29 Sun (Gov Diri) — Reuters (24 Sat)
  + Dateline/Prima News (29 Sun, Tinubu ₦250m aid). ✓
- Cikande: 3 confirmed dead, 24 body bags recovered Sun evening,
  34 missing — Reuters + AP + Xinhua + People/detikNews. ✓ (See §6 P1:
  the morning snapshot 3/36/7 is superseded by the evening state.)
- Kyiv drone Sun, 14 missing — Straits Times via Hansen Intel. ✓
- Bolsonaro stable in ICU, day 2 — HeadlinesXtra + One Turn, 22 Nov. ✓
- Delta: >half of flights delayed, 6% cancelled, fixed by evening —
  CNN 22 Nov (FlightAware: 58% delayed). ✓
- Korea minister quits Sun — Reuters (filed 23 Nov, event Sun) +
  Korea JoongAng Daily + Guardian. ✓
- Manipur: official toll 17 Sun (16 Chandel + 1 Kakching), 228 in
  hospital — TechWord News + NE Insider (The Hindu) + Daily Kiran. ✓
  (fact.net.in reports 18; the image uses the official 17 — see §6 P2.)
- Florida: river at 18.72 ft Sun morning, above the 17.55 ft 1953
  record — The Florida Press 22 Nov; record broke Thu 19 Nov per
  Florida Today. ✓ (Wording fixed in §6 P1: "holds at a new all-time
  high", not "near" the old record.)
- AFCON 2027 host cities — Kawowo + Mozzart Sport: CAF confirmed six
  cities Sat 21 Nov (Nairobi, Dar es Salaam, Arusha, Zanzibar,
  Kampala, Hoima). ✓
- Shuri Castle ceremony Sun 22 Nov, opens Mon — Meaningful.News. ✓
- Houthi missiles intercepted Sat — Reuters + TBS + Al Jazeera. ✓
- U17 Sunday scores, Juventus 4–0, Iraq Basra fire, England 37–12,
  ICJ, Shenzhen summit, Akvan, GTA VI, UK–EU, Nasdaq, Riemann,
  EU–Indonesia — all carried/verified as in SOURCES.md. ✓
- Weekday verified: 22 Nov 2026 is a Sunday.
- **Gaza Board of Peace line — REMOVED (§6 P0).** The report was
  delivered to the UNSC on Tue 17 Nov (AP, Reuters 18 Nov); the Al
  Jazeera page's 22 Nov timestamp was a republication, not the event
  date. The slot now holds Shuri Castle (verified Sunday).

## 4. STORY COUNT + REGIONS (recounted from the data tables)

1 lead + 3 heroes + 16 smalls + 20 also-on = **40** ✓ (eyebrow says 40).
Regions: EUROPE 13 · ASIA 9 · MIDDLE EAST 4 · N. AMERICA 7 · AFRICA 2 ·
S. AMERICA 1 · GLOBAL 4 = 40 ✓ (assignments listed in SOURCES.md).
Africa is now 2 stories (Nigeria boat + AFCON hosts). Oceania is 0 —
the only Oceania candidates (Australia T20, the NZ venue of the India
Test) were cut or counted by team; recorded as a known weakness.

## 5. DESIGN DISCUSSION (helper subagent, before the rebuild)

A design-discussion helper read the brief, the late-Sunday docs and
the data tables, ran fresh web checks, and delivered a ranked story
set and placement rationale (analysis only — no entry text/code).
Its recommendations were adopted: heroes Liverpool + Alcaraz + India;
Barça + Bahrain demoted to smalls (attribution needs a panel, not a
hero headline); numbers strip rebuilt as an all-Sunday scoreboard
(4–0, 720/9, 352, 5–0, 3–2, 251.3, 36→34, 14); also-on slots bought
by merging lines, not adding rows; Africa fixed via AFCON hosts
(2 stories) rather than the unverified RFI reprisal report. Two
judgement calls went against the helper: (a) the helper missed the
Delta system failure, which the builder's own research found (CNN)
and promoted to a small; (b) the helper advised keeping Manipur at
11/180+ and not updating to 16/600 — the builder used the Sunday
official count 17/228 instead (see §6 P2). The helper also warned
against printing any Cikande body-bag count as a death toll — adopted.

## 6. POST-BUILD REVIEW (helper subagent, after the rebuild) + FIXES

A post-build review helper re-ran the gate itself (draw script twice
+ main.ts twice, same sha256), recounted stories/regions, spot-checked
19 facts with fresh searches, and inspected the image at full size,
300 px and 2× crops. Verdict: CONDITIONAL PASS. Findings and fixes:

- **P0 — Gaza also-on line misdated.** The Board of Peace report was
  delivered Tue 17 Nov; the Al Jazeera page timestamp (22 Nov) was a
  republication. A 5-day-old story tagged SUN is a criterion-1 risk.
  FIXED: line replaced with Shuri Castle (verified Sunday); DATE CHECK
  now names the Tue 17 Nov report as a trap; SOURCES.md's "page
  timestamp = event date" reasoning corrected and the error recorded.
- **P1 — Cikande panel understated the day's end state.** The panel
  used the Sunday-morning snapshot (3 dead, 36 missing, 7 body bags);
  by Sunday evening police had removed 24 body bags and 34 remained
  missing (Reuters/AP/Xinhua/detikNews). SOURCES.md's claim that "24"
  was unverifiable was factually wrong. FIXED: panel now reads
  "3 DEAD, 34 MISSING" + "24 body bags recovered by Sunday evening;
  the toll is unclear — one bag may hold remains of several people";
  numbers strip 36→34; SOURCES.md corrected with a retraction note.
- **P1 — Florida wording misframed the record.** "Still near its
  73-year record high" understates a river sitting a foot ABOVE the
  old record. FIXED: line now reads "holds at a new all-time high".
  (The Thu 19 Nov record-break day is sourced to Florida Today; other
  trackers' Fri dating appears to reflect a different gauge.)
- **P2 — Manipur toll picked the contested higher figure.** The
  official Sunday count is 17; "18" comes from one outlet's Chandel
  count. FIXED: line now uses the official 17 / 228 in hospital;
  SOURCES.md explains the 17-vs-18 discrepancy.
- **P2 — Craft: smalls bodies crossed panel borders.** The guard
  checked line counts only. FIXED: pitch fix + new vertical-extent
  guard (see §2 D2); verified by 2× crop.
- **P2 — Numbers-strip label repeated the numeral.** FIXED: "STRØM
  251.3 PTS" → "STRØM WINS".
- **Process:** the helper noted the committed REVIEW.md /
  REBUILD_NOTES.md still described the late-Sunday edition (it read
  them before the builder's rewrite landed). FIXED: both files are
  rewritten for the final edition in this commit; REVIEW.md §5/§6
  now exist and describe the helper rounds.
- Accepted, not fixed: sport is ~40% of the page and the also-on
  block is majority pre-Sunday — Sunday genuinely was a huge sport
  day and the also-on header honestly frames the block as "Sunday
  22 Nov & the weekend that led here"; the merged Akvan/Peru and
  Real/Roma lines are terse but verified.

## 7. SKILLS USED / USELESS (SKILLS RULE)

- **frontend-design** — used: one-bold-element discipline, date
  honesty as the mechanism, top-of-page-proves-Sunday, copy
  minimalism. Its generic-default warnings were checked against the
  broadsheet brief (the brief pins the broadsheet look, so the
  "generic broadsheet" caution does not apply here).
- **verification-before-completion** — used: every completion claim
  in this review rests on a command run in this session (draw script
  twice + sha256, main.ts twice + cmp, PIL load, 2× crop inspection,
  fresh web searches for the fixed facts).
- **requesting-code-review** — used in spirit: the post-build review
  helper round is the code/content review for this entry (the skill's
  git-SHA dispatch template was adapted — the reviewer ran the gate
  itself and spot-checked 19 facts).
- **writing-plans / executing-plans** — not read in full this round:
  the refresh checklist in REBUILD_NOTES.md already served as the
  plan, and the work was a data-table edit, not a multi-phase build.
- **test-driven-development / webapp-testing** — useless for this
  bounty: no test harness, no web app; the overflow guard + determinism
  runs are the entry's tests.
- **systematic-debugging** — not needed: no bug was debugged beyond
  the guard-caught overflows, which the guard itself diagnosed.
- **find-skills** — used only to confirm the skill list; no new skill
  was needed.
- **content skills (social-content, copywriting)** — not used: the
  bounty needs faithful news copy, not creative/copywriting work.
- **Relay models (Apinex / 100milionseek)** — NOT used: no spend.
  All research was direct web search by the builder + helpers.
