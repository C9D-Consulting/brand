#!/usr/bin/env python3
"""c9d_pdf_build.py: build a C9D Consulting branded PDF (The Dossier) from a markdown
source with YAML front matter. Same source dialect and front matter as c9d_docx_build.py.

Usage:  python3 c9d_pdf_build.py source.md out.pdf [--mode screen|print] [--verify]
Modes:  screen  The Dossier dark ground, for PDFs read on screen (default).
        print   Light-mode tokens on white paper, for anything printed, signed or bound.
        Both: US Letter, 1.0in / 1.5in margins, 5.5in text block, 13.5pt body.
Tokens: palettes, the attribution line, the measure and the typeface names are read from
        the brand repo's tokens.json (--tokens PATH, $C9D_TOKENS, ./tokens.json beside this
        script, or fetched from github.com/C9D-Consulting/brand). Nothing is compiled in.
Needs:  pip install weasyprint fonttools   (poppler-utils for --verify)
Fonts:  fetched from the Google Fonts repository on first run into ./fonts beside this
        script (Inter Tight, JetBrains Mono, Instrument Serif; all SIL OFL), instanced to
        static weights. Same cache and file names as c9d_docx_build.py, so the two scripts
        can share one ./fonts folder. WeasyPrint subsets and embeds every face used.

Front matter keys: file_id, classification, title, subtitle, prepared_for, prepared_by,
version, section_marker. Body: # title, ## "EYEBROW · Title" sections (a bare number
renders as SECTION 01), ### and #### subheads, GFM tables, - and 1. lists, **bold**,
*italic*, `mono`, and [bracketed placeholders], which render in stamp amber.
"""
import re, sys, os, html, shutil, subprocess, statistics, collections

VERSION = "1.2"

# ---- tokens: read from the brand repo's tokens.json, never compiled in -------------------
# Resolution order: --tokens PATH, $C9D_TOKENS, the repo copy when this script runs from the
# brand repo's generators/ folder, tokens.json beside this script, then the
# source of record on GitHub (cached beside this script). No fallback palette exists here:
# if tokens.json cannot be found the build stops, so a token change is made once, in the repo.
TOKENS_URL = ("https://raw.githubusercontent.com/C9D-Consulting/brand/main/"
              "c9d-consulting-brand/assets/tokens.json")
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = {}   # filled by load_tokens(): palettes, attribution, measure, families

def load_tokens(path=None, refresh=False):
    import json, urllib.request
    repo = os.path.join(HERE, "..", "c9d-consulting-brand", "assets", "tokens.json")
    cands = [path, os.environ.get("C9D_TOKENS"), repo, os.path.join(HERE, "tokens.json")]
    src = next((c for c in cands if c and os.path.exists(c)), None)
    cache = os.path.join(HERE, "tokens.json")
    if src is None or refresh:
        try:
            data = urllib.request.urlopen(TOKENS_URL, timeout=20).read()
            open(cache, "wb").write(data); src = cache
        except Exception as e:
            if src is None:
                sys.exit(f"tokens.json not found and could not be fetched ({e}). "
                         "Pass --tokens path/to/c9d-consulting-brand/assets/tokens.json.")
    d = json.load(open(src, encoding="utf8"))
    def pal(mode):
        c = d["color"][mode]
        v = lambda grp, k: c[grp][k]["value"]
        return dict(bg=v("ground", "bg"), bg2=v("ground", "bg-2"), bg3=v("ground", "bg-3"),
                    rule=v("rule", "rule"), rule_bright=v("rule", "rule-bright"),
                    ink_bright=v("ink", "ink-bright"), ink=v("ink", "ink"),
                    ink_mute=v("ink", "ink-mute"), ink_dim=v("ink", "ink-dim"),
                    stamp=v("signal", "stamp"), stamp_dim=v("signal", "stamp-dim"),
                    classified=v("crit", "classified"))
    screen, prnt = pal("dark"), pal("light")
    # Print is ink on paper: the page stays white so office printers need no full bleed.
    # Every other print colour, including the header fill (bg-2), comes from the light map.
    prnt["page"] = "#ffffff"; screen["page"] = screen["bg"]
    st = d["typography"]["stack"]
    BRAND.update(
        source=src, token_version=d["$metadata"].get("version", "?"),
        palettes={"screen": screen, "print": prnt},
        attribution=d["naming"]["founder"]["attribution"],
        measure=int(d["spatial"]["measure"]["max-body-chars"]),
        families=(st["display"]["family"], st["mono"]["family"], st["italic-accent"]["family"]))
    missing = [f for f in BRAND["families"] if f not in {k[0] for k in FONT_FILES}]
    if missing:
        sys.exit(f"tokens.json names typefaces this script cannot embed: {missing}")
    return BRAND

# ---- fonts (same instancing and file names as c9d_docx_build.py) ------------------------
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_FILES = {  # (css family, weight, style) -> file
    ("Inter Tight", 300, "normal"): "InterTightLight-Regular.ttf",
    ("Inter Tight", 400, "normal"): "InterTight-Regular.ttf",
    ("Inter Tight", 500, "normal"): "InterTightMedium-Regular.ttf",
    ("Inter Tight", 600, "normal"): "InterTightSemiBold-Regular.ttf",
    ("JetBrains Mono", 500, "normal"): "JetBrainsMonoMedium-Regular.ttf",
    ("JetBrains Mono", 600, "normal"): "JetBrainsMonoSemiBold-Regular.ttf",
    ("Instrument Serif", 400, "italic"): "InstrumentSerif-Italic.ttf",
}
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl"
GF_FILES = {
    "InterTight[wght].ttf": "intertight/InterTight%5Bwght%5D.ttf",
    "JetBrainsMono[wght].ttf": "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
    "InstrumentSerif-Italic.ttf": "instrumentserif/InstrumentSerif-Italic.ttf",
}

def ensure_fonts():
    if all(os.path.exists(os.path.join(FONT_DIR, f)) for f in FONT_FILES.values()):
        return
    import urllib.request
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    src = os.path.join(FONT_DIR, "_src"); os.makedirs(src, exist_ok=True)
    for local, remote in GF_FILES.items():
        p = os.path.join(src, local)
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"{GF}/{remote}", p)
    def inst(local, wght, out):
        f = instancer.instantiateVariableFont(TTFont(os.path.join(src, local)), {"wght": wght})
        f["OS/2"].usWeightClass = wght
        f.save(os.path.join(FONT_DIR, out))
    for (fam, w, _), out in FONT_FILES.items():
        if fam == "Inter Tight": inst("InterTight[wght].ttf", w, out)
        elif fam == "JetBrains Mono": inst("JetBrainsMono[wght].ttf", w, out)
    shutil.copy(os.path.join(src, "InstrumentSerif-Italic.ttf"),
                os.path.join(FONT_DIR, FONT_FILES[("Instrument Serif", 400, "italic")]))

# ---- markdown parsing (identical dialect to c9d_docx_build.py) --------------------------
def parse_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.index("\n---", 3)
        for line in text[3:end].strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        text = text[end + 4:]
    return meta, text

INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\])")

def inline_runs(text):
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("**"): yield "bold", part[2:-2]
        elif part.startswith("*"): yield "italic", part[1:-1]
        elif part.startswith("`"): yield "mono", part[1:-1]
        elif part.startswith("[") and part.endswith("]") and not part.startswith("[["):
            yield "placeholder", part
        else: yield "body", part

def parse_blocks(text):
    lines = text.splitlines()
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows)); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            blocks.append(("h%d" % len(m.group(1)), m.group(2).strip())); i += 1; continue
        if re.match(r"^- ", ln):
            items = []
            while i < len(lines) and re.match(r"^- ", lines[i]):
                items.append(lines[i][2:].strip()); i += 1
            blocks.append(("ul", items)); continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]).strip()); i += 1
            blocks.append(("ol", items)); continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\d+\. )", lines[i]):
            para.append(lines[i].strip()); i += 1
        blocks.append(("p", " ".join(para)))
    return blocks

# ---- html rendering ---------------------------------------------------------------------
E = html.escape

def inline_html(text):
    out = []
    for kind, t in inline_runs(text):
        t = E(t, quote=False)
        if kind == "bold": out.append(f"<strong>{t}</strong>")
        elif kind == "italic": out.append(f"<em>{t}</em>")
        elif kind == "mono": out.append(f"<code>{t}</code>")
        elif kind == "placeholder": out.append(f'<span class="ph">{t}</span>')
        else: out.append(t)
    return "".join(out)

def table_html(rows):
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    weights = []
    for j in range(ncols):  # proportion columns to content, header sets the floor
        body_max = max([len(re.sub(r"[*`\[\]]", "", r[j])) for r in rows[1:]] or [0])
        body_word = max([len(w) for r in rows[1:] for w in re.sub(r"[*`\[\]]", "", r[j]).split()] or [0])
        head_word = max([len(w) for w in rows[0][j].split()] or [0])
        # never narrower than the longest word in the column: words must not split
        weights.append(max(len(rows[0][j]) * 1.7 + 3, head_word * 2.0 + 3,
                           min(body_max, 60) ** 0.85, body_word * 1.25 + 2, 6))
    tot = sum(weights)
    cls = "tbl keep" if len(rows) <= 8 else "tbl"
    h = [f'<table class="{cls}"><colgroup>']
    h += [f'<col style="width:{100 * w / tot:.2f}%">' for w in weights]
    h.append("</colgroup><thead><tr>")
    h += [f"<th>{E(c)}</th>" for c in rows[0]]
    h.append("</tr></thead><tbody>")
    for r in rows[1:]:
        h.append("<tr>" + "".join(f"<td>{inline_html(c)}</td>" for c in r) + "</tr>")
    h.append("</tbody></table>")
    return "".join(h)

def body_html(blocks):
    out = []
    for idx, (kind, val) in enumerate(blocks):
        nxt = blocks[idx + 1][0] if idx + 1 < len(blocks) else None
        if kind == "h1":
            out.append(f'<h1 class="doc-title">{inline_html(val)}</h1><div class="rule"></div>')
        elif kind == "h2":
            if " · " in val:
                eyebrow, title = val.split(" · ", 1)
                if re.fullmatch(r"\d+", eyebrow): eyebrow = f"SECTION {int(eyebrow):02d}"
            else:
                eyebrow, title = "SECTION", val
                if re.match(r"^\d+\.\s", val):
                    print(f"warning: '## {val}' should be '## N · Title'", file=sys.stderr)
            out.append(f'<section class="sec"><div class="eyebrow">{E(eyebrow)}</div>'
                       f'<h2>{inline_html(title)}</h2><div class="rule"></div></section>')
        elif kind == "h3":
            out.append(f"<h3>{inline_html(val)}</h3>")
        elif kind == "h4":
            out.append(f"<h4>{inline_html(val)}</h4>")
        elif kind == "p":
            if val.startswith("*") and val.endswith("*") and not val.startswith("**"):
                out.append(f'<p class="desc">{E(val[1:-1], quote=False)}</p>')
            else:
                keep = " keep-next" if (len(val) <= 60 or nxt == "table") else ""
                out.append(f'<p class="body{keep}">{inline_html(val)}</p>')
        elif kind in ("ul", "ol"):
            items = "".join(f"<li>{inline_html(it)}</li>" for it in val)
            out.append(f"<{kind}>{items}</{kind}>")
        elif kind == "table":
            out.append(table_html(val))
    return "\n".join(out)

def cover_html(m):
    rows = [("DOCUMENT", m.get("title", "")), ("PREPARED FOR", m.get("prepared_for", "")),
            ("PREPARED BY", m.get("prepared_by", "")),
            ("CLASSIFICATION", m.get("classification", "")), ("VERSION", m.get("version", ""))]
    meta = "".join(f'<tr><td class="k">{E(k)}</td><td class="v">{E(v)}</td></tr>' for k, v in rows)
    return f"""<div class="cover">
  <div class="c-id">{E(m.get('file_id', ''))}</div>
  <div class="c-class">{E(m.get('classification', ''))}</div>
  <div class="c-title">{E(m.get('title', ''))}</div>
  <div class="c-rule"></div>
  <div class="c-sub">{E(m.get('subtitle', ''))}</div>
  <table class="c-meta">{meta}</table>
  <div class="c-foot"><div class="wm big"><span class="c9d">C9D</span> Consulting</div>
    <div class="attr">{E(BRAND["attribution"])}</div></div>
</div>"""

def css(mode, meta):
    t = BRAND["palettes"][mode]
    faces = "\n".join(
        f'@font-face {{ font-family: "{fam}"; font-weight: {w}; font-style: {s}; '
        f'src: url("file://{os.path.join(FONT_DIR, f)}"); }}'
        for (fam, w, s), f in FONT_FILES.items())
    q = lambda s: '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    marker = meta.get("section_marker", "01")
    return f"""{faces}
@page {{
  size: letter; margin: 1.0in 1.5in 1.0in 1.5in; background: {t['page']};
  @top-left {{ content: {q(meta.get('file_id', ''))}; width: 1.85in; vertical-align: bottom; white-space: nowrap;
    font: 500 8pt "JetBrains Mono"; letter-spacing: .04em; color: {t['ink_mute']};
    border-bottom: .5pt solid {t['rule']}; padding-bottom: 5pt; margin-bottom: 18pt; }}
  @top-center {{ content: {q(meta.get('classification', '').upper())}; width: 1.8in; vertical-align: bottom; white-space: nowrap;
    font: 500 8pt "Inter Tight"; letter-spacing: .18em; color: {t['stamp']};
    border-bottom: .5pt solid {t['rule']}; padding-bottom: 5pt; margin-bottom: 18pt; }}
  @top-right {{ content: {q('§ ' + marker + ' · ')} counter(page) " / " counter(pages); width: 1.85in; white-space: nowrap;
    vertical-align: bottom; text-align: right;
    font: 500 8pt "JetBrains Mono"; letter-spacing: .04em; color: {t['ink_mute']};
    border-bottom: .5pt solid {t['rule']}; padding-bottom: 5pt; margin-bottom: 18pt; }}
  @bottom-left {{ content: element(footer); width: 5.5in; vertical-align: top; }}
}}
@page :first {{
  @top-left {{ content: none; border: 0; }} @top-center {{ content: none; border: 0; }}
  @top-right {{ content: none; border: 0; }} @bottom-left {{ content: none; }}
}}
html {{ background: {t['page']}; }}
body {{ margin: 0; font: 400 13.5pt/1.6 "Inter Tight"; color: {t['ink']};
  font-kerning: normal; hyphens: manual; text-align: left; orphans: 2; widows: 2; }}
strong {{ font-weight: 600; color: {t['ink_bright']}; }}
em {{ font-family: "Instrument Serif"; font-style: italic; font-size: 1.04em; color: {t['ink_bright']}; }}
code {{ font: 500 .92em "JetBrains Mono"; color: {t["ink"]}; white-space: nowrap; }}
.ph {{ color: {t['stamp']}; }}
.c9d {{ color: {t['stamp']}; }}

#footer {{ position: running(footer); border-top: .5pt solid {t['rule']}; padding-top: 5pt;
  margin-top: 18pt; display: table; width: 5.5in; table-layout: fixed; }}
#footer > div {{ display: table-cell; font-size: 9pt; line-height: 1.2; color: {t['ink_mute']}; }}
#footer .f1 {{ width: 1.6in; font-size: 10pt; color: {t['ink']}; letter-spacing: -.02em; }}
#footer .f2 {{ width: 2.3in; text-align: center; }}
#footer .f3 {{ width: 1.6in; text-align: right; font-family: "JetBrains Mono"; font-weight: 500; letter-spacing: .04em; }}

.cover {{ position: relative; height: 9.0in; page-break-after: always; bookmark-level: none; }}
.c-id {{ margin-top: 36pt; font: 500 11pt/1.3 "JetBrains Mono"; letter-spacing: .04em; color: {t['ink_mute']}; }}
.c-class {{ font: 500 9pt/1.3 "Inter Tight"; letter-spacing: .18em; text-transform: uppercase; color: {t['stamp']}; }}
.c-title {{ margin-top: 78pt; font: 300 36pt/1.05 "Inter Tight"; letter-spacing: -.03em; color: {t['ink_bright']}; }}
.c-rule {{ margin-top: 10pt; width: 1.75in; border-bottom: 1pt solid {t['rule_bright']}; }}
.c-sub {{ margin-top: 16pt; font: 300 18pt/1.3 "Inter Tight"; color: {t['ink_mute']}; }}
.c-meta {{ margin-top: 72pt; width: 100%; border-collapse: collapse; }}
.c-meta td {{ padding: 5pt 10pt 5pt 0; border-bottom: .5pt solid {t['rule']}; vertical-align: top; }}
.c-meta .k {{ width: 1.45in; font: 500 10pt/1.3 "JetBrains Mono"; letter-spacing: .10em; color: {t['ink_mute']}; }}
.c-meta .v {{ font: 400 12pt/1.3 "Inter Tight"; color: {t['ink']}; }}
.c-foot {{ position: absolute; bottom: 0; left: 0; }}
.wm.big {{ font: 400 16pt/1.2 "Inter Tight"; letter-spacing: -.04em; color: {t['ink_bright']}; }}
.attr {{ margin-top: 2pt; font: 400 10pt/1.2 "Inter Tight"; color: {t['ink_mute']}; }}

h1, h2, h3, h4 {{ margin: 0; font-weight: 300; color: {t['ink_bright']}; break-after: avoid; }}
h1.doc-title {{ font-size: 24pt; line-height: 1.1; letter-spacing: -.02em; margin-bottom: 6pt; bookmark-level: 1; }}
.rule {{ border-bottom: .5pt solid {t['rule_bright']}; margin-bottom: 12pt; break-after: avoid; }}
section.sec {{ break-inside: avoid; break-after: avoid; margin-top: 28pt; }}
.eyebrow {{ font: 600 10pt/1.3 "JetBrains Mono"; letter-spacing: .18em; text-transform: uppercase;
  color: {t['stamp']}; margin-bottom: 4pt; }}
section.sec h2 {{ font-size: 24pt; line-height: 1.1; letter-spacing: -.02em; margin-bottom: 6pt; bookmark-level: 2; }}
h3 {{ font-size: 18pt; line-height: 1.2; letter-spacing: -.01em; margin: 18pt 0 6pt; bookmark-level: 3; }}
h4 {{ font-weight: 500; font-size: 14pt; line-height: 1.3; margin: 12pt 0 4pt; bookmark-level: none; }}
p {{ margin: 0 0 10pt; }}
p.keep-next {{ break-after: avoid; }}
p.desc {{ font-weight: 300; color: {t['ink_mute']}; }}
ul, ol {{ margin: 0 0 10pt; padding: 0; list-style: none; }}
li {{ position: relative; padding-left: .4in; margin-bottom: 6pt; line-height: 1.5; break-inside: avoid; }}
ul > li::before {{ content: "–"; position: absolute; left: 0; color: {t['stamp_dim']}; }}
ol {{ counter-reset: n; }}
ol > li {{ counter-increment: n; }}
ol > li::before {{ content: counter(n, decimal-leading-zero) "."; position: absolute; left: 0;
  font: 500 10pt/1.8 "JetBrains Mono"; color: {t['stamp_dim']}; }}
table.tbl {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin: 2pt 0 14pt; }}
table.tbl.keep {{ break-inside: avoid; }}
table.tbl tr {{ break-inside: avoid; }}
table.tbl th {{ background: {t['bg2']}; border-bottom: 1pt solid {t['rule_bright']};
  font: 600 9pt/1.4 "JetBrains Mono"; letter-spacing: .18em; text-transform: uppercase;
  color: {t['stamp_dim'] if mode == 'print' else t['stamp']}; text-align: left; padding: 6pt 7pt; }}
table.tbl td {{ border-bottom: .5pt solid {t['rule']}; font-size: 10pt; line-height: 1.4;
  padding: 6pt 7pt; vertical-align: top; }}
table.tbl th:first-child, table.tbl td:first-child {{ padding-left: 5pt; }}
table.tbl th:last-child, table.tbl td:last-child {{ padding-right: 5pt; }}
"""

def build_html(meta, blocks, mode):
    footer = ('<div id="footer"><div class="f1"><span class="c9d">C9D</span> Consulting</div>'
              f'<div class="f2">{E(BRAND["attribution"])}</div>'
              '<div class="f3">c9d.consulting</div></div>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{E(meta.get('title', ''))}</title>
<meta name="author" content="{E(meta.get('prepared_by', 'Brandon Wilburn, C9D Consulting'))}">
<meta name="description" content="{E(meta.get('subtitle', ''))}">
<meta name="keywords" content="{E(meta.get('file_id', ''))}, {E(meta.get('classification', ''))}">
<meta name="generator" content="c9d_pdf_build.py {VERSION} ({mode})">
<style>{css(mode, meta)}</style></head><body>
{footer}
{cover_html(meta)}
{body_html(blocks)}
</body></html>"""

# ---- source lint (voice and dialect) ---------------------------------------------------
def lint(meta, body):
    issues = []
    missing = [k for k in ("file_id", "classification", "title", "subtitle", "prepared_for",
                           "prepared_by", "version", "section_marker") if not meta.get(k)]
    if missing: issues.append("front matter missing: " + ", ".join(missing))
    full = body + " " + " ".join(meta.values())
    if "\u2014" in full: issues.append(f"em-dash x{full.count(chr(0x2014))}")
    bare = re.findall(r"\bC9D\b(?! Consulting)", full)
    if bare: issues.append(f"bare 'C9D' x{len(bare)}")
    ph = re.findall(r"(?<!\[)\[[^\]\[]+\](?!\])", body)
    if ph: issues.append(f"unresolved [placeholders] x{len(ph)} (fine for a template, not for a delivered file)")
    if re.search(r"^---\s*$", body, re.M): issues.append("'---' rule in body (strip it)")
    if re.search(r"<[a-zA-Z/][^>]*>", body): issues.append("HTML in body")
    if re.search(r"^>\s", body, re.M): issues.append("block quote (not in dialect)")
    if re.search(r"^[ \t]+(-|\d+\.) ", body, re.M): issues.append("indented or nested list (not in dialect)")
    return issues

# ---- verification ------------------------------------------------------------------------
def md_words(body):
    body = re.sub(r"^#+\s*", "", body, flags=re.M)
    body = re.sub(r"^\|?\s*:?-{3,}.*$", "", body, flags=re.M)
    body = re.sub(r"[*`|]", " ", body)
    return [w.lower() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.,:;%$&/()\-]*", body)]

def norm(ws):
    return collections.Counter(re.sub(r"[^a-z0-9]", "", w) for w in ws if re.sub(r"[^a-z0-9]", "", w))

def verify(pdf, body):
    ok = True
    fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    def embedded(f):
        m = re.search(r"\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", f)
        return bool(m) and m.group(1) == "yes"
    bad = [f for f in fonts if not re.search(r"Inter-?Tight|JetBrains-?Mono|Instrument-?Serif", f)
           or not embedded(f)]
    names = sorted({re.sub(r"^[A-Z]{6}\+", "", f.split()[0]) for f in fonts})
    print("fonts:", ", ".join(names))
    if bad: ok = False; print("FAIL fonts not brand or not embedded:\n  " + "\n  ".join(bad))
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = txt.split("\f")
    lens = [len(l.strip()) for p in pages[1:] for l in p.splitlines()
            if len(l.strip()) > 40 and not re.search(r"§|" + re.escape(BRAND["attribution"]) + r"|\s{3,}", l.strip())]
    if lens:
        med = statistics.median(lens)
        print(f"measure: median body line {med:.0f} chars over {len(lens)} lines")
        if med > BRAND["measure"]: ok = False; print(f"FAIL measure over {BRAND['measure']}")
    raw = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    attr = BRAND["attribution"]
    n_attr = raw.count(attr)
    stray = re.findall(re.escape(attr) + r"(?=[.,;:])", raw)
    print(f"attribution: '{attr}' x{n_attr} (tokens.json)")
    if n_attr < 2: ok = False; print("FAIL attribution missing from cover or footer")
    if stray: ok = False; print(f"FAIL attribution carries trailing punctuation x{len(stray)}")
    have = norm(re.findall(r"\S+", raw.lower()))
    need = norm(md_words(body))
    miss = {w: n - have.get(w, 0) for w, n in need.items() if have.get(w, 0) < n}
    miss = {w: n for w, n in miss.items() if not re.fullmatch(r"\d+", w)}  # section numbers become eyebrows
    print(f"parity: {sum(need.values())} source words, {sum(miss.values())} missing")
    if miss: ok = False; print("FAIL missing words:", dict(list(miss.items())[:20]))
    print(f"pages: {len(pages) - 1 if pages[-1].strip() == '' else len(pages)}")
    print("VERIFY", "PASS" if ok else "FAIL")
    return ok

# ---- main ---------------------------------------------------------------------------------
def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source"); ap.add_argument("out")
    ap.add_argument("--mode", choices=["screen", "print"], default="screen")
    ap.add_argument("--tokens", help="path to tokens.json (default: beside the script, else fetched from the brand repo)")
    ap.add_argument("--refresh-tokens", action="store_true", help="re-fetch tokens.json from the brand repo")
    ap.add_argument("--verify", action="store_true", help="fonts, measure, parity report")
    ap.add_argument("--html", action="store_true", help="also write the intermediate HTML")
    a = ap.parse_args()
    src, out, mode = a.source, a.out, a.mode
    flags = [f for f, on in (("--verify", a.verify), ("--html", a.html)) if on]
    load_tokens(a.tokens, a.refresh_tokens)
    print(f"tokens: {BRAND['source']} (v{BRAND['token_version']})")
    text = open(src, encoding="utf8").read()
    meta, body = parse_front_matter(text)
    for issue in lint(meta, body):
        print("lint:", issue, file=sys.stderr)
    os.makedirs(FONT_DIR, exist_ok=True)
    ensure_fonts()
    doc = build_html(meta, parse_blocks(body), mode)
    if "--html" in flags:
        open(out + ".html", "w", encoding="utf8").write(doc)
    import logging; logging.getLogger("weasyprint").setLevel(logging.ERROR)
    from weasyprint import HTML
    opts = dict(pdf_tags=True, custom_metadata=True)
    try:
        HTML(string=doc, base_url=os.getcwd()).write_pdf(out, **opts)
    except TypeError:
        HTML(string=doc, base_url=os.getcwd()).write_pdf(out)
    print(f"wrote {out} ({mode}) {os.path.getsize(out) // 1024} KB")
    if "--verify" in flags:
        sys.exit(0 if verify(out, body) else 1)

if __name__ == "__main__":
    main()
