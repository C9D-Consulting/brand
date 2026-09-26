#!/usr/bin/env python3
"""Generate database icons in the C9D Consulting Dossier system.

Not pictograms. Each icon is a record-type code set in JetBrains Mono on Ground, inside a
1px-equivalent bordered box: the sanctioned classification-stamp form from section 4 of the
PowerPoint guidelines. The code carries information, which is what the brand requires of chrome.

Tokens used: Ground 0C0B08, Rule 2A2620, Ink D8CDB8, Ink Mute 8A7E6A, Stamp D6743A.
Signal is rationed. Stamp marks only the three records that carry the practice's proof.
"""
import os
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
def _font(name, legacy):
    """Prefer the fonts vendored beside this script, fall back to the old /tmp paths."""
    local = os.path.join(_HERE, "fonts", name)
    return local if os.path.exists(local) else legacy


SIZE   = 512
GROUND = (0x0C, 0x0B, 0x08)
RULE   = (0x2A, 0x26, 0x20)
INK    = (0xD8, 0xCD, 0xB8)
INKMUT = (0x8A, 0x7E, 0x6A)
STAMP  = (0xD6, 0x74, 0x3A)

FONT = _font("JetBrainsMono-SemiBold.ttf", "/tmp/jbm/fonts/ttf/JetBrainsMono-SemiBold.ttf")
OUT  = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders", "notion-icons")

# key, two-letter code, ink token, border token
ICONS = [
 ("engagements",        "EN", STAMP,  STAMP),
 ("placements",         "PL", INK,    RULE),
 ("acceptance",         "AC", INK,    RULE),
 ("raid",               "RA", INK,    RULE),
 ("change_requests",    "CR", INK,    RULE),
 ("document_register",  "DR", INK,    RULE),
 ("client_actions",     "CA", INK,    RULE),
 ("retrospectives",     "RE", INK,    RULE),
 ("agreements",         "AG", INK,    RULE),
 ("bench_requests",     "BR", INK,    RULE),
 ("candidates",         "CN", INK,    RULE),
 ("partners",           "PF", INKMUT, RULE),
 ("bill_rate_bands",    "RB", INK,    RULE),
 ("templates",          "TP", INK,    RULE),
 ("evidence",           "EV", STAMP,  STAMP),
 ("people",             "RO", INK,    RULE),
 ("domains",            "DM", INK,    RULE),
 ("credentials",        "OC", STAMP,  STAMP),
 ("gaps",               "GP", INK,    RULE),
 ("development_plans",  "DP", INK,    RULE),
 ("certifications",     "CT", INK,    RULE),
 ("partner_benefits",   "PB", INK,    RULE),
 ("learning_resources", "LR", INK,    RULE),
 ("partner_programs",   "PP", INK,    RULE),
]

# page and template-row icons: same form as the database icons, keyed by the page they sit on
PAGES = [
 ("page-origination-program",  "OP", INK, RULE),   # Firm, Origination Program (FILE-NTN-2026-023)
 ("tpl-origination-agreement", "OA", INK, RULE),   # Templates row, Master Origination Agreement
 ("tpl-registration-form",     "RF", INK, RULE),   # Templates row, Opportunity Registration Form
 ("tpl-term-sheet",            "TS", INK, RULE),   # Templates row, Origination Program Term Sheet
]

# the seven teamspace anchors, as section markers
ANCHORS = [
 ("anchor-firm",             "01", INK, RULE),
 ("anchor-practice",         "02", INK, RULE),
 ("anchor-enablement",       "03", INK, RULE),
 ("anchor-delivery",         "04", INK, RULE),
 ("anchor-partner-network",  "05", INK, RULE),
 ("anchor-client-portals",   "06", INK, RULE),
 ("anchor-partner-exchange", "07", INK, RULE),
]


def tracked_width(draw, text, font, tracking):
    w = 0
    for i, ch in enumerate(text):
        w += draw.textlength(ch, font=font)
        if i < len(text) - 1:
            w += tracking
    return w


def render(code, ink, border, path, section=False):
    img = Image.new("RGB", (SIZE, SIZE), GROUND)
    d = ImageDraw.Draw(img)

    # 1px-equivalent hairline box. Rendered at 16px so it survives to roughly 1px on screen.
    inset, weight = 26, 16
    d.rectangle([inset, inset, SIZE - inset - 1, SIZE - inset - 1], outline=border, width=weight)

    size = 210 if not section else 190
    font = ImageFont.truetype(FONT, size)
    tracking = size * 0.18          # +0.18em, the mono chrome tracking from the brand
    text = code
    tw = tracked_width(d, text, font, tracking)
    bbox = d.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    x = (SIZE - tw) / 2
    y = (SIZE - th) / 2 - bbox[1]

    for i, ch in enumerate(text):
        d.text((x, y), ch, font=font, fill=ink)
        x += d.textlength(ch, font=font) + tracking

    if section:
        # the section-marker glyph, small, above the number
        sf = ImageFont.truetype(FONT, 78)
        sw = d.textlength("§", font=sf)
        d.text(((SIZE - sw) / 2, 92), "§", font=sf, fill=border if border != RULE else INKMUT)

    img.save(path, "PNG")
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for key, code, ink, border in ICONS:
        p = os.path.join(OUT, "%s.png" % key)
        render(code, ink, border, p)
        made.append((key, code, p))
    for key, code, ink, border in PAGES:
        p = os.path.join(OUT, "%s.png" % key)
        render(code, ink, border, p)
        made.append((key, code, p))
    for key, num, ink, border in ANCHORS:
        p = os.path.join(OUT, "%s.png" % key)
        render(num, ink, border, p, section=True)
        made.append((key, "§ " + num, p))
    print("generated %d icons in %s" % (len(made), OUT))
    for k, c, _ in made:
        print("  %-24s %s" % (k, c))

    # contact sheet for review, at true display size alongside a large sample
    cols, cell = 8, 128
    rows = (len(made) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * cell + 160), GROUND)
    for i, (k, c, p) in enumerate(made):
        im = Image.open(p).resize((cell - 24, cell - 24), Image.LANCZOS)
        sheet.paste(im, ((i % cols) * cell + 12, (i // cols) * cell + 12))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 22)
    d.text((14, rows * cell + 18), "AT DISPLAY SIZE", font=f, fill=INKMUT)
    x = 14
    for key, code, ink, border in ICONS[:10]:
        im = Image.open(os.path.join(OUT, "%s.png" % key)).resize((20, 20), Image.LANCZOS)
        sheet.paste(im, (x, rows * cell + 58)); x += 30
        im2 = Image.open(os.path.join(OUT, "%s.png" % key)).resize((28, 28), Image.LANCZOS)
        sheet.paste(im2, (x, rows * cell + 54)); x += 42
    sheet.save(os.path.join(OUT, "contact-sheet.png"))
    print("\ncontact sheet: brand/contact-sheet.png")


if __name__ == "__main__":
    main()
