#!/usr/bin/env python3
"""Platform logo plates in the C9D Consulting Dossier system.

Some platforms do not take a lockup, they take a fixed-size image slot and render it at exactly
that size. Google Workspace is the first of them: the Admin console logo is displayed at exactly
320x132, PNG or GIF, 30KB maximum, and it appears in the top left of Gmail, Calendar and Drive for
every user in the tenant. Dropping a transparent wordmark into that slot leaves the mark floating
in whatever chrome the product happens to use, so the slot gets a composed plate instead: the
locked lockup on brand ground, with clear space, sized to the slot.

The lockup is never redrawn. It is rendered from the locked SVG in assets/logos, trimmed to its
ink box, and placed. That is the whole reason this is a generator rather than a hand-made PNG.

Composition rules, traceable to the logo README and c9d-consulting-pptx-guidelines v1.0:
  L4  The wordmark colours are locked. The dark plate is Stamp on Ground, the light plate is the
      light-mode pairing on the light Ground. The plate recolours nothing; it only places.
  L6  Do not modify the wordmark. No shadow, no glow, no outline, no skew, no rotation. The
      lockup is scaled uniformly and composited, nothing else.
  s2  Stamp is signal, not decoration. It arrives inside the lockup and nowhere else on the plate.
  s7  No imagery. The plate is the mark on ground, which is the brand working rather than a gap.
  s9  No colour outside the token set.

Vertical placement. Centring the ink box would count the descender on the "g" as mass and sit the
mark high in the slot, with a visible gap underneath. The cap-to-baseline block is what reads as
the wordmark, so the baseline is measured off the leading cap, which has no descender, and that
block is centred instead. The descender hangs below. The build asserts the result.

Dark is the default for every platform plate, because The Dossier is dark by default and a
self-contained dark plate reads against both light and dark product chrome. The light plate is the
alternate for a platform whose chrome makes the dark block read heavy.

Requires Pillow and cairosvg.
"""
import io
import os

import cairosvg
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
LOGOS = os.path.join(_ROOT, "c9d-consulting-brand", "assets", "logos")

GROUND       = "#0c0b08"             # --bg
GROUND_LIGHT = "#f5f1e8"             # --bg-light, print and light-mode surfaces

RENDER_W = 2400                      # supersample the lockup before the downscale
PALETTE  = 128                       # quantise; the plate is flat ground plus antialiased type

# key, source lockup, ground, canvas, lockup width inside the canvas, size ceiling in bytes
PLATES = [
    (
        "c9d-banner-google-workspace-320x132.png",
        "c9d-consulting-wordmark-horizontal-dark.svg",
        GROUND, (320, 132), 256, 30 * 1024,
    ),
    (
        "c9d-banner-google-workspace-light-320x132.png",
        "c9d-consulting-wordmark-horizontal-light.svg",
        GROUND_LIGHT, (320, 132), 256, 30 * 1024,
    ),
]


def ink_box(svg_path):
    """The lockup rendered large and trimmed to its ink, with nothing else touched."""
    png = cairosvg.svg2png(url=svg_path, output_width=RENDER_W, background_color=None)
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    return img.crop(img.getbbox())


def baseline_fraction(ink):
    """Where the baseline sits in the ink box, as a fraction of its height.

    Measured off the leading cap, which carries no descender, so the fraction holds for any
    lockup in the set rather than being a constant tuned to one string.
    """
    w, h = ink.size
    lead = ink.crop((0, 0, max(1, int(w * 0.08)), h))
    return lead.getbbox()[3] / h


def plate(out_name, svg_name, ground, canvas, lockup_w, ceiling):
    ink = ink_box(os.path.join(LOGOS, svg_name))
    bl = baseline_fraction(ink)

    cw, ch = canvas
    h = max(1, round(ink.height * (lockup_w / ink.width)))
    ink = ink.resize((lockup_w, h), Image.LANCZOS)

    x = (cw - lockup_w) // 2
    y = round(ch / 2 - (bl * h) / 2)              # baseline on the centre line, descender hangs

    img = Image.new("RGBA", canvas, ground)
    img.alpha_composite(ink, (x, y))
    out = os.path.join(LOGOS, out_name)
    img.convert("RGB").quantize(colors=PALETTE, dither=Image.NONE).save(out, "PNG", optimize=True)

    baseline = y + round(bl * h)
    cap_centre = (y + baseline) / 2               # centre of the cap-to-baseline block
    size = os.path.getsize(out)
    assert Image.open(out).size == canvas, f"{out_name} is not {cw}x{ch}"
    assert abs(cap_centre - ch / 2) <= 1, f"{out_name} cap block centred at {cap_centre}, not {ch/2}"
    cap = baseline - y                            # cap height, the clear space unit
    assert min(x, cw - x - lockup_w) >= cap, f"{out_name} has under one cap height of side clear space"
    assert min(y, ch - baseline) >= cap, f"{out_name} has under one cap height of vertical clear space"
    assert size <= ceiling, f"{out_name} is {size} bytes, over the {ceiling} byte platform ceiling"
    print(f"{out_name}  lockup {lockup_w}x{h} at ({x},{y})  cap block {y}-{baseline}  {size/1024:.1f}KB")


if __name__ == "__main__":
    for spec in PLATES:
        plate(*spec)
