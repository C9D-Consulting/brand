#!/usr/bin/env python3
"""Shared drive theme banners in the C9D Consulting Dossier system.

Google renders a shared drive theme twice from one image. The full 1280x144 canvas is the banner
across the top of the drive. Only the centre band, x 550 to 730, becomes the small thumbnail in
the shared drives list, at roughly 40px. Anything outside that band is invisible in the list, and
anything smaller than about a two-character glyph is unreadable at 40px.

So the composition is three zones:

  x    0 to 500   the drive name, right aligned, Inter Tight Light, Ink Bright   (banner only)
  x  550 to 730   the record code in a 1px hairline box                          (banner + thumbnail)
  x  780 to 1280  the classification stamp, left aligned                         (banner only)

The centre code is the same form as the Notion database icons: a two-letter code in JetBrains Mono
inside a hairline box, on Ground. That keeps one visual language across Notion and Drive.

Rules applied, traceable to c9d-consulting-pptx-guidelines v1.0:
  s2  Stamp is reserved. No drive holds the practice's proof, so every code is Ink on a Rule box.
      The one exception is the classification on the client drive, which is a genuine distribution
      marker rather than decoration.
  s3  Display is Inter Tight at light weight with negative tracking. Mono carries chrome only.
  s4  Classification stamps are mono, uppercase, letter-spaced, in a 1px-bordered box.
  s4  Hairlines are 1px, Rule colour, never thicker and never coloured.
  s7  No imagery. The banner is type and rules, which is the brand working rather than a gap.
  s9  No light backgrounds, no accent bars, no colour outside the token set.
"""
import os
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
def _font(name, legacy):
    """Prefer the fonts vendored beside this script, fall back to the old /tmp paths."""
    local = os.path.join(_HERE, "fonts", name)
    return local if os.path.exists(local) else legacy


W, H = 1280, 144
THUMB_L, THUMB_R = 550, 730          # the band Google crops for the list thumbnail
CX, CY = 640, 72

GROUND     = (0x0C, 0x0B, 0x08)
RULE       = (0x2A, 0x26, 0x20)
INK_BRIGHT = (0xF0, 0xE6, 0xD0)
INK        = (0xD8, 0xCD, 0xB8)
INK_MUTE   = (0x8A, 0x7E, 0x6A)
STAMP      = (0xD6, 0x74, 0x3A)

MONO  = _font("JetBrainsMono-Regular.ttf",  "/tmp/jbm/fonts/ttf/JetBrainsMono-Regular.ttf")
MONOB = _font("JetBrainsMono-SemiBold.ttf", "/tmp/jbm/fonts/ttf/JetBrainsMono-SemiBold.ttf")
INTER = _font("InterTight.ttf",             "/tmp/intertight/InterTight.ttf")
OUT   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders", "drive-themes")

NAME_PT, CODE_PT, STAMP_PT = 30, 46, 15
MONO_TRACK, NAME_TRACK, NAME_WEIGHT = 0.18, -0.03, 300

BOX = 104                            # the hairline box, inside the 180px thumbnail band

# key, code, drive name, classification, stamp is signal
THEMES = [
 ("firm",       "FM", "C9D CONSULTING: FIRM",       "INTERNAL",           False),
 ("practice",   "PR", "C9D CONSULTING: PRACTICE",   "INTERNAL",           False),
 ("commercial", "CM", "C9D CONSULTING: COMMERCIAL", "INTERNAL",           False),
 ("delivery",   "DL", "C9D CONSULTING: DELIVERY",   "INTERNAL",           False),
 ("client",     "CL", "CLIENT",                     "CLIENT CONFIDENTIAL", True),
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

def render(code, name, classification, signal, path):
    img = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(img)

    f_name  = inter(NAME_PT)
    f_code  = ImageFont.truetype(MONOB, CODE_PT)
    f_stamp = ImageFont.truetype(MONO, STAMP_PT)
    tr_name, tr_code, tr_stamp = NAME_PT * NAME_TRACK, CODE_PT * MONO_TRACK, STAMP_PT * MONO_TRACK

    # centre: the record code in a hairline box. This is the only zone the thumbnail shows.
    d.rectangle([CX - BOX // 2, CY - BOX // 2, CX + BOX // 2, CY + BOX // 2], outline=RULE, width=1)
    cw = measure(d, code, f_code, tr_code)
    put(d, code, f_code, tr_code, CX - cw / 2, CY - CODE_PT * 0.72, INK)

    # left: the drive name, right aligned, clear of the thumbnail band
    nw = measure(d, name, f_name, tr_name)
    put(d, name, f_name, tr_name, 500 - nw, CY - NAME_PT * 0.70, INK_BRIGHT)

    # right: the classification stamp in a 1px-bordered box
    col = STAMP if signal else INK_MUTE
    sw = measure(d, classification, f_stamp, tr_stamp)
    px, py = 14, 9
    x0, y0 = 780, CY - (STAMP_PT + py * 2) / 2
    d.rectangle([x0, y0, x0 + sw + px * 2, y0 + STAMP_PT + py * 2], outline=col, width=1)
    put(d, classification, f_stamp, tr_stamp, x0 + px, y0 + py - 3, col)

    assert 500 - nw > 8, "%s: name overruns the canvas" % name
    assert x0 + sw + px * 2 < W - 8, "%s: classification overruns the canvas" % name
    img.save(path, "PNG")

def main():
    os.makedirs(OUT, exist_ok=True)
    for key, code, name, cls, signal in THEMES:
        p = os.path.join(OUT, "drive-%s.png" % key)
        render(code, name, cls, signal, p)
        print("  %-12s %s" % (key, p))
    print("generated %d theme banners at %dx%d" % (len(THEMES), W, H))

if __name__ == "__main__":
    main()
