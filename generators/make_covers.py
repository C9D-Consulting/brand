#!/usr/bin/env python3
"""Cover banners in the C9D Consulting Dossier system.

Built to the locked visual system as translated in c9d-consulting-pptx-guidelines v1.0. The
closest sanctioned analogue to a page cover is Layout 02, the section divider: oversized section
mark in Stamp mono, plus the title as Display L. That is what this renders.

Rules applied, each traceable to the guidelines:
  s2  Stamp D6743A carries section markers. This is a sanctioned signal use, not decoration.
  s3  Display type is Inter Tight at light weight with negative tracking. Mono is metadata only,
      so the section name is Inter Tight Light, never mono. The deck never uses bold display type.
  s3  Mono chrome is uppercase at +0.18em tracking. That applies to the mark and the stamp only.
  s4  A classification stamp is mono, uppercase, letter-spaced, inside a 1px-bordered box, with a
      Stamp border for standard distribution and a Classified border only for a refusal or crit
      finding. Nothing here is either, so every border is Stamp.
  s4  Hairlines are 1px, Rule colour, never thicker and never coloured.
  s9  No bold display type, no accent bars, no colour outside the token set.

Positioning. Notion crops a cover to whatever box the viewport gives it, anchored on the centre.
A web column is wide and short, so the sides survive. A phone is narrow, so the sides are lost,
and the app puts its back, share and overflow buttons over the top corners while the page icon
sits over the bottom left on both. The masthead is therefore centred on both axes inside a safe
box of the middle 44 percent of the width and 40 percent of the height, which is what every
viewport has in common. The build asserts every cover fits that box.
"""
import os
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
def _font(name, legacy):
    """Prefer the fonts vendored beside this script, fall back to the old /tmp paths."""
    local = os.path.join(_HERE, "fonts", name)
    return local if os.path.exists(local) else legacy


W, H   = 1500, 600
CX, CY = W // 2, H // 2
SAFE_W, SAFE_H = int(W * 0.44), int(H * 0.40)

GROUND     = (0x0C, 0x0B, 0x08)
RULE       = (0x2A, 0x26, 0x20)
INK_BRIGHT = (0xF0, 0xE6, 0xD0)
INK        = (0xD8, 0xCD, 0xB8)
INK_MUTE   = (0x8A, 0x7E, 0x6A)
INK_DIM    = (0x5A, 0x50, 0x42)
STAMP      = (0xD6, 0x74, 0x3A)

MONO  = _font("JetBrainsMono-Regular.ttf", "/tmp/jbm/fonts/ttf/JetBrainsMono-Regular.ttf")
INTER = _font("InterTight.ttf",            "/tmp/intertight/InterTight.ttf")
OUT   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders", "notion-covers")

NAME_PT, MARK_PT, STAMP_PT = 46, 21, 17
MONO_TRACK  =  0.18      # s3 mono chrome tracking
NAME_TRACK  = -0.03      # s3 negative tracking on display
NAME_WEIGHT = 300        # s3 display weights are light

# key, locator, name, classification
#
# s4 distinguishes two pieces of chrome. A section marker (mono, Stamp) states position in a
# sequence; a file ID (mono, Ink Dim) locates the document. The seven teamspaces are sections and
# take the mark. The template and container pages are not sections, so they take their file ID
# instead of a section number that would point at nothing.
COVERS = [
 ("firm",              "section", "01",                "FIRM",                  "INTERNAL"),
 ("practice",          "section", "02",                "PRACTICE",              "INTERNAL"),
 ("enablement",        "section", "03",                "ENABLEMENT",            "INTERNAL"),
 ("delivery",          "section", "04",                "DELIVERY",              "INTERNAL"),
 ("partner-network",   "section", "05",                "PARTNER NETWORK",       "INTERNAL"),
 ("client-portals",    "section", "06",                "CLIENT PORTALS",        "INTERNAL"),
 ("partner-exchange",  "section", "07",                "PARTNER EXCHANGE",      "INTERNAL"),
 ("tpl-engagement",    "file",    "FILE-NTN-2026-020", "ENGAGEMENT WORKSPACE",  "TEMPLATE"),
 ("tpl-client-portal", "file",    "FILE-NTN-2026-021", "CLIENT PORTAL",         "TEMPLATE"),
 ("tpl-partner-exch",  "file",    "FILE-NTN-2026-022", "PARTNER EXCHANGE",      "TEMPLATE"),
 ("engagement-spaces", "file",    "FILE-NTN-2026-023", "ENGAGEMENT WORKSPACES", "INTERNAL"),
]

def inter(size, weight=NAME_WEIGHT):
    f = ImageFont.truetype(INTER, size)
    f.set_variation_by_axes([weight])
    return f

def measure(d, text, font, tracking):
    w = 0
    for i, ch in enumerate(text):
        w += d.textlength(ch, font=font)
        if i < len(text) - 1:
            w += tracking
    return w

def put(d, text, font, tracking, x, y, fill):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x

def render(kind, locator, name, classification, path):
    img = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(img)

    f_mark  = ImageFont.truetype(MONO, MARK_PT)
    f_stamp = ImageFont.truetype(MONO, STAMP_PT)
    f_name  = inter(NAME_PT)
    tr_mark, tr_stamp = MARK_PT * MONO_TRACK, STAMP_PT * MONO_TRACK
    tr_name = NAME_PT * NAME_TRACK

    # s4 section marker is Stamp; a file ID is Ink Dim
    top_txt = ("§ %s" % locator) if kind == "section" else locator
    top_col = STAMP if kind == "section" else INK_DIM
    mw = measure(d, top_txt, f_mark, tr_mark)
    put(d, top_txt, f_mark, tr_mark, CX - mw / 2, CY - 96, top_col)

    # s3 title: Inter Tight Light, negative tracking, Ink Bright
    nw = measure(d, name, f_name, tr_name)
    put(d, name, f_name, tr_name, CX - nw / 2, CY - 50, INK_BRIGHT)

    # s4 hairline, 1px, Rule
    d.rectangle([CX - nw / 2, CY + 22, CX + nw / 2, CY + 22], fill=RULE)

    # s4 classification stamp: mono uppercase letter-spaced in a 1px-bordered box, Stamp border
    sw = measure(d, classification, f_stamp, tr_stamp)
    pad_x, pad_y = 18, 11
    bx0, by0 = CX - sw / 2 - pad_x, CY + 46
    bx1, by1 = CX + sw / 2 + pad_x, CY + 46 + STAMP_PT + pad_y * 2
    d.rectangle([bx0, by0, bx1, by1], outline=STAMP, width=1)
    put(d, classification, f_stamp, tr_stamp, CX - sw / 2, by0 + pad_y - 3, STAMP)

    blk_w, blk_h = max(nw, bx1 - bx0, mw), by1 - (CY - 96)
    assert blk_w <= SAFE_W, "%s: %dpx wide, safe box %d" % (name, blk_w, SAFE_W)
    assert blk_h <= SAFE_H, "%s: %dpx tall, safe box %d" % (name, blk_h, SAFE_H)
    img.save(path, "PNG")
    return blk_w, blk_h

def main():
    os.makedirs(OUT, exist_ok=True)
    for key, kind, locator, name, cls in COVERS:
        p = os.path.join(OUT, "cover-%s.png" % key)
        w, h = render(kind, locator, name, cls, p)
        print("  %-20s %4dx%-4d  safe %dx%d" % (key, w, h, SAFE_W, SAFE_H))
    print("generated %d covers" % len(COVERS))

if __name__ == "__main__":
    main()
