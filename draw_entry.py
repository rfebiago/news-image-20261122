#!/usr/bin/env python3
"""news-image-20261122 — final edition.

Draws a dense broadsheet front page (1024x1024 PNG) summing up the
world's news of Sunday 22 November 2026. Pure stdlib + Pillow, no
network, no randomness, no clock: the same run always writes the same
bytes. Edit ONLY the DATA tables below to change the stories; the
layout code underneath never changes for a data refresh
(except the smalls pitch + vertical guard added in the post-review fix;
see REBUILD_NOTES.md).

Run:  python3 draw_entry.py        # writes entry.png next to this file
The script exits non-zero on ANY text overflow — fix the copy, never
silence the guard.
"""

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
MARGIN = 26
CW = W - 2 * MARGIN  # 972

PAPER = (246, 241, 227)
INK = (22, 21, 19)
RED = (166, 30, 20)
NAVY = (30, 58, 92)
GREY = (107, 101, 88)
RULE = (201, 191, 166)
PANEL = (255, 253, 246)
LEAD_BG = (238, 231, 214)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines (never empty)."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def fit_lines(draw, text, fnt_path, size, max_w, max_lines, shrink_to=8):
    """Wrap text, shrinking the font until it fits max_lines. Raises on failure."""
    s = size
    while s >= shrink_to:
        fnt = font(fnt_path, s)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines and all(
            text_w(draw, ln, fnt) <= max_w for ln in lines
        ):
            return fnt, lines
        s -= 1
    raise SystemExit(f"OVERFLOW: cannot fit in {max_lines} lines: {text!r}")


def one_line(draw, text, fnt, max_w, label):
    if text_w(draw, text, fnt) > max_w:
        raise SystemExit(f"OVERFLOW ({label}): {text!r}")
    return text


# ---------------------------------------------------------------- DATA
EYEBROW_L = "THE WORLD IN ONE PAGE  ·  40 STORIES, EVERY ONE DATED"
EYEBROW_R = "FINAL EDITION"
KICKER = "COP31 COLLAPSES  ·  LIVERPOOL 4–0 MAN UTD  ·  ALCARAZ WINS IN TURIN  ·  INDIA 720/9"

NUMBERS = [
    ("4–0", "BEAT MAN UTD"),
    ("720/9", "INDIA, RECORD IN NZ"),
    ("352", "INDIA'S LEAD"),
    ("5–0", "ALCARAZ UNBEATEN"),
    ("3–2", "BARÇA COMEBACK"),
    ("251.3", "STRØM WINS"),
    ("34", "MISSING IN CIKANDE"),
    ("14", "MISSING IN KYIV"),
]

# tag, headline, body
LEAD = (
    "SUN 22 NOV  ·  ANTALYA — CLIMATE",
    "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
    "After two days in overtime, the Antalya pact was rejected at the closing plenary: "
    "the EU and others refused a text with no mention of fossil fuels. Guterres called it "
    "deeply disappointing; the summit ends with no deal.",
)

HEROES = [
    (
        "SUN 22 NOV  ·  WELLINGTON — CRICKET",
        "INDIA 720/9: BIGGEST TEST TOTAL EVER IN NEW ZEALAND",
        "Pant 128 as India declare, 352 ahead; NZ 119/2 at stumps, "
        "still 233 behind.",
    ),
    (
        "SUN 22 NOV  ·  ANFIELD — FOOTBALL",
        "LIVERPOOL THRASH MAN UTD 4–0 IN POCHETTINO'S DEBUT",
        "Yoro sent off after 8 minutes; Liverpool 2–0 up in 13 and "
        "never look back. United stay 19th.",
    ),
    (
        "SUN 22 NOV  ·  TURIN — TENNIS",
        "ALCARAZ BEATS ZVEREV TO WIN FIRST ATP FINALS TITLE",
        "Wins 6–2, 7–6(7), saving three set points; first Spaniard "
        "to lift the trophy in 28 years.",
    ),
]

# tag, headline, body — 16 panels, 4 columns x 4 rows
SMALLS = [
    ("SUN 22 NOV  ·  BARCELONA",
     "BARÇA COME BACK FROM 0–2 TO WIN 3–2",
     "Villarreal led 2–0 at half-time; Barcelona turn it round to stay top, three clear of Real."),
    ("SUN 22 NOV  ·  MANAMA",
     "BAHRAIN: TWO HURT AS IRAN STRIKE HITS CIVILIAN SITE",
     "Bahrain says Iran's Saturday attack set fire to a site in Sitra; Iran claims US bases hit."),
    ("SUN 22 NOV  ·  HULL",
     "HULL STUN BRIGHTON 2–0 WITH LATE DOUBLE",
     "McBurnie scores twice in stoppage time; Brighton miss the chance to close on leaders Arsenal."),
    ("SAT 21 NOV  ·  CIKANDE",
     "CANDY FACTORY FIRE: 3 DEAD, 34 MISSING",
     "24 body bags recovered by Sunday evening; the toll is unclear — one bag may hold remains of several people."),
    ("SUN 22 NOV  ·  HONG KONG",
     "WANG WINS HK OPEN; ANTONSEN BY WALKOVER",
     "Wang Zhiyi beats Pornpawee 21–16, 21–11. Kunlavut withdraws hurt, so Antonsen takes the men's title without playing."),
    ("SUN 22 NOV  ·  LILLEHAMMER",
     "STRØM WINS AT HOME; NORWAY SWEEP AGAIN",
     "Anna Odine Strøm 251.3 pts tops Kvandal and Westvold Hansen — a second straight all-Norwegian podium."),
    ("SUN 22 NOV  ·  KYIV REGION",
     "DRONE COLLAPSES FLAT BLOCK; 14 MISSING",
     "A Russian drone hits a five-storey home near Kyiv on Sunday morning; rescuers search the rubble."),
    ("FRI 20 NOV  ·  BAYELSA",
     "FUNERAL BOAT SINKS; TOLL RISES TO 29",
     "Boat capsizes on the way to a burial; governor confirms 29 dead Sunday, 51 survivors; Tinubu gives ₦250m aid."),
    ("SAT 21 NOV  ·  BRASÍLIA",
     "BOLSONARO STABLE IN INTENSIVE CARE",
     "Ex-president remains in ICU on day two, conscious and stable; doctors have not ruled out surgery."),
    ("SUN 22 NOV  ·  WEST BANK",
     "ISRAELI OPPOSITION CALLS SETTLER ARSON 'TERRORISM'",
     "Gadi Eisenkot condemns suspected settler attacks; Hamas calls an IDF tunnel operation a ceasefire breach."),
    ("SAT 21 NOV  ·  WASHINGTON",
     "FBI PROBES APPARENT HACK OF ITS CRIME DATABASE",
     "Trump confirms the National Crime Information Center was targeted; the FBI is investigating the breach."),
    ("SUN 22 NOV  ·  ATLANTA",
     "DELTA SYSTEM FAILURE DELAYS HALF ITS FLIGHTS",
     "A weight-and-balance glitch delays more than half of Delta's flights nationwide; the system is fixed by evening."),
    ("SUN 22 NOV  ·  SEOUL",
     "KOREA MINISTER QUITS IN AI-CHEATING ROW",
     "Choi Kyo-jin resigns over last-minute anti-cheating rules for the entrance exam; Lee accepts within the hour."),
    ("SAT 21 NOV  ·  LAS VEGAS",
     "VERSTAPPEN WINS IN VEGAS — 75TH F1 WIN",
     "Fifty laps, 35 lead changes: Verstappen holds off Norris by 0.639s; Piastri third. Russell hits the wall late."),
    ("FRI 20 NOV NIGHT  ·  SINALOA",
     "FBI'S MOST-WANTED CARTEL BOSS CAUGHT",
     "'El Chapo Isidro' seized in Guasave; 11 killed in the raid, four of them soldiers. $5m US reward."),
    ("SAT 21 NOV  ·  RIYADH",
     "HOUTHI MISSILES AT RIYADH INTERCEPTED",
     "Saudi-led coalition says three Houthi ballistic missiles aimed at Riyadh were stopped; it strikes Hodeidah port."),
]

# tag, text — 20 lines, split 10 + 10 across two columns
ALSO_ON = [
    ("SUN", "Juventus 4–0 Venezia in Turin."),
    ("SUN", "U17 WC: Greece 2–1 Panama; Saudi Arabia 1–0 France."),
    ("SUN", "U17 WC: Denmark 0–0 Australia; Argentina 1–0 Mozambique."),
    ("SAT", "Iraq: fire at Basra power station kills 4, injures 35."),
    ("SUN", "India: toxic alcohol toll rises to 17 in Manipur, 228 in hospital."),
    ("SUN", "Florida: St Johns River holds at a new all-time high."),
    ("SAT", "Chelsea 1–4 Leeds; Newcastle 2–2 Arsenal."),
    ("SAT", "Man City 1–1 Fulham; Bournemouth win 9th straight."),
    ("SAT", "Real Madrid 2–1 Celta; Roma 5–1 Parma, Malen scores four."),
    ("SAT", "England 37–12 All Blacks; biggest ever win over New Zealand."),
    ("THU", "ICJ: Myanmar guilty of genocide over the Rohingya."),
    ("THU", "First Trump–Xi–Putin summit, Shenzhen — no Ukraine deal."),
    ("FRI", "Cyclone Akvan: 372,000 evacuated, 0 dead; Peru quake M6.7."),
    ("FRI", "GTA VI: $3.79bn in sales on day one."),
    ("FRI", "UK–EU reset signed — but only if tuition deal follows."),
    ("FRI", "AI rout: Nasdaq –5.3%, Nvidia –14% in a day."),
    ("SAT", "CAF names six AFCON 2027 host cities; Nairobi Kenya's only host."),
    ("SUN", "Shuri Castle rises again; opens to the public Monday."),
    ("SAT", "AI 'proves' Riemann — independent checks confirm the claim."),
    ("SAT", "EU–Indonesia trade deal signed after 10 years of talks."),
]

REGIONS = "EUROPE 13  ·  ASIA 9  ·  MIDDLE EAST 4  ·  N. AMERICA 7  ·  AFRICA 2  ·  S. AMERICA 1  ·  GLOBAL 4"

DATE_CHECK = (
    "DATE CHECK — NOT TODAY'S NEWS: ICJ ruling Thu 19 Nov · Shenzhen Thu 19 Nov · Akvan landfall, "
    "Nasdaq rout, GTA VI figure — all Fri 20 Nov · Chapo Isidro caught Fri 20 Nov night · "
    "St Johns record broke Thu 19 Nov · Gaza Board of Peace report Tue 17 Nov · "
    "IND–NZ day 5 is Mon 23 Nov, not Sunday."
)
BUILD_LINE = (
    "Built from verified sources — see SOURCES.md in the repo. Final edition, 23 Nov 2026."
)


# ---------------------------------------------------------------- LAYOUT
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- eyebrow ------------------------------------------------------
    f_eyebrow = font(SANS_B, 13)
    one_line(d, EYEBROW_L, f_eyebrow, CW - 260, "eyebrow-L")
    d.text((MARGIN, 16), EYEBROW_L, font=f_eyebrow, fill=NAVY)
    f_eyebrow_r = font(SANS_B, 13)
    rw = text_w(d, EYEBROW_R, f_eyebrow_r)
    d.text((W - MARGIN - rw, 16), EYEBROW_R, font=f_eyebrow_r, fill=RED)

    # --- masthead -----------------------------------------------------
    f_mast = font(SERIF, 92)
    d.text((MARGIN - 4, 34), "THE WORLD", font=f_mast, fill=INK)
    f_date1 = font(SERIF, 46)
    f_date2 = font(SANS_B, 27)
    t1, t2 = "SUNDAY", "22 NOVEMBER 2026"
    w1, w2 = text_w(d, t1, f_date1), text_w(d, t2, f_date2)
    d.text((W - MARGIN - w1, 40), t1, font=f_date1, fill=RED)
    d.text((W - MARGIN - w2, 92), t2, font=f_date2, fill=RED)
    d.line([(MARGIN, 136), (W - MARGIN, 136)], fill=INK, width=3)
    d.line([(MARGIN, 141), (W - MARGIN, 141)], fill=INK, width=1)

    # --- kicker -------------------------------------------------------
    f_kicker = font(SANS_B, 15)
    one_line(d, KICKER, f_kicker, CW, "kicker")
    d.text((MARGIN, 150), KICKER, font=f_kicker, fill=NAVY)

    # --- numbers strip ------------------------------------------------
    y0, y1 = 172, 216
    cell_w = CW / len(NUMBERS)
    d.rectangle([MARGIN, y0, W - MARGIN, y1], outline=RULE, width=1)
    for i, (num, label) in enumerate(NUMBERS):
        x = MARGIN + i * cell_w
        if i:
            d.line([(x, y0), (x, y1)], fill=RULE, width=1)
        f_num = font(SERIF, 25)
        f_lab = font(SANS_B, 9)
        nw = text_w(d, num, f_num)
        if nw > cell_w - 8:
            raise SystemExit(f"OVERFLOW (numbers): {num!r}")
        d.text((x + (cell_w - nw) / 2, y0 + 4), num, font=f_num, fill=RED)
        lab_lines = wrap(d, label, f_lab, cell_w - 10)
        if len(lab_lines) > 1:
            raise SystemExit(f"OVERFLOW (numbers label): {label!r}")
        ly = y0 + 33
        for ln in lab_lines:
            lw = text_w(d, ln, f_lab)
            d.text((x + (cell_w - lw) / 2, ly), ln, font=f_lab, fill=INK)
            ly += 11

    # --- lead hero (full width) ---------------------------------------
    ly0, ly1 = 224, 318
    d.rectangle([MARGIN, ly0, W - MARGIN, ly1], fill=LEAD_BG, outline=INK, width=2)
    f_tag = font(SANS_B, 12)
    d.text((MARGIN + 12, ly0 + 8), LEAD[0], font=f_tag, fill=RED)
    f_head, head_lines = fit_lines(d, LEAD[1], SERIF, 33, CW - 24, 1)
    hy = ly0 + 28
    for ln in head_lines:
        d.text((MARGIN + 12, hy), ln, font=f_head, fill=INK)
        hy += 38
    f_body = font(SANS, 14)
    body_lines = wrap(d, LEAD[2], f_body, CW - 24)
    if len(body_lines) > 2:
        raise SystemExit(f"OVERFLOW (lead body): {len(body_lines)} lines")
    by = ly0 + 62
    for ln in body_lines:
        d.text((MARGIN + 12, by), ln, font=f_body, fill=INK)
        by += 18

    # --- three heroes --------------------------------------------------
    hy0, hy1 = 326, 446
    hero_w = (CW - 24) / 3
    for i, (tag, headline, body) in enumerate(HEROES):
        x0 = MARGIN + i * (hero_w + 12)
        x1 = x0 + hero_w
        d.rectangle([x0, hy0, x1, hy1], fill=PANEL, outline=INK, width=1)
        d.text((x0 + 10, hy0 + 7), tag, font=font(SANS_B, 10), fill=RED)
        f_h, h_lines = fit_lines(d, headline, SERIF, 20, hero_w - 20, 2)
        yy = hy0 + 26
        for ln in h_lines:
            d.text((x0 + 10, yy), ln, font=f_h, fill=INK)
            yy += 24
        f_b = font(SANS, 11)
        b_lines = wrap(d, body, f_b, hero_w - 20)
        if len(b_lines) > 3:
            raise SystemExit(f"OVERFLOW (hero {i} body): {len(b_lines)} lines")
        for ln in b_lines:
            d.text((x0 + 10, yy), ln, font=f_b, fill=INK)
            yy += 14
        if yy > hy1 - 4:
            raise SystemExit(f"OVERFLOW (hero {i} box): text ends {yy - hy1}px past box")

    # --- smalls grid 4 x 4 ---------------------------------------------
    gy0 = 454
    col_w = (CW - 24) / 4
    row_h = 84
    for idx, (tag, headline, body) in enumerate(SMALLS):
        r, c = divmod(idx, 4)
        x0 = MARGIN + c * (col_w + 8)
        y = gy0 + r * row_h
        d.rectangle([x0, y, x0 + col_w, y + row_h - 6], fill=PANEL, outline=RULE, width=1)
        d.text((x0 + 8, y + 4), tag, font=font(SANS_B, 9), fill=RED)
        f_h, h_lines = fit_lines(d, headline, SANS_B, 12, col_w - 16, 2)
        yy = y + 16
        for ln in h_lines:
            d.text((x0 + 8, yy), ln, font=f_h, fill=INK)
            yy += 13
        f_b = font(SANS, 10)
        b_lines = wrap(d, body, f_b, col_w - 16)
        if len(b_lines) > 3:
            raise SystemExit(f"OVERFLOW (small {idx} body): {len(b_lines)} lines: {body!r}")
        for ln in b_lines:
            d.text((x0 + 8, yy), ln, font=f_b, fill=INK)
            yy += 11
        if yy > y + row_h - 6:
            raise SystemExit(f"OVERFLOW (small {idx} box): text ends {yy - (y + row_h - 6)}px past box")

    # --- also-on --------------------------------------------------------
    ay0 = 794
    f_ao_head = font(SANS_B, 13)
    d.text((MARGIN, ay0), "ALSO ON — SUNDAY 22 NOV & THE WEEKEND THAT LED HERE",
           font=f_ao_head, fill=NAVY)
    d.line([(MARGIN, ay0 + 18), (W - MARGIN, ay0 + 18)], fill=INK, width=2)
    f_tag2 = font(SANS_B, 11)
    f_txt = font(SANS, 12)
    col2_w = (CW - 16) / 2
    for idx, (tag, text) in enumerate(ALSO_ON):
        col, row = divmod(idx, 10)
        x0 = MARGIN + col * (col2_w + 16)
        y = ay0 + 24 + row * 13
        tag_txt = tag + "  "
        tw = text_w(d, tag_txt, f_tag2)
        if tw + text_w(d, text, f_txt) > col2_w:
            raise SystemExit(f"OVERFLOW (also-on {idx}): {text!r}")
        d.text((x0, y), tag_txt, font=f_tag2, fill=RED)
        d.text((x0 + tw, y), text, font=f_txt, fill=INK)

    # --- date-check footer (regions tally lives in SOURCES.md) ---------
    fy0 = ay0 + 24 + 10 * 13 + 6
    f_dc = font(SANS, 11)
    dc_lines = wrap(d, DATE_CHECK, f_dc, CW - 20)
    if len(dc_lines) > 3:
        raise SystemExit(f"OVERFLOW (date check): {len(dc_lines)} lines")
    fy1 = fy0 + 10 + len(dc_lines) * 14 + 8
    d.rectangle([MARGIN, fy0, W - MARGIN, fy1], outline=RED, width=2)
    d.text((MARGIN + 10, fy0 + 4), "DATE CHECK — READ BEFORE YOU QUOTE",
           font=font(SANS_B, 11), fill=RED)
    yy = fy0 + 20
    for ln in dc_lines:
        d.text((MARGIN + 10, yy), ln, font=f_dc, fill=INK)
        yy += 14
    f_build = font(SANS, 10)
    d.text((MARGIN, fy1 + 6), BUILD_LINE, font=f_build, fill=GREY)
    if fy1 + 20 > H - 4:
        raise SystemExit("OVERFLOW (footer past page bottom)")

    img.save(OUT, format="PNG", optimize=True)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"wrote {OUT} {OUT.stat().st_size} bytes sha256={digest}")
    print(f"stories: 1 lead + {len(HEROES)} heroes + {len(SMALLS)} smalls "
          f"+ {len(ALSO_ON)} also-on = {1 + len(HEROES) + len(SMALLS) + len(ALSO_ON)}")


if __name__ == "__main__":
    main()
