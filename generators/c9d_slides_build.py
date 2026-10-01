#!/usr/bin/env python3
"""C9D Consulting HTML deck build (The Dossier, slide mode).

Markdown with front matter in, one self-contained HTML deck out.

  python3 c9d_slides_build.py deck.md deck.html                     # standalone deck, fonts embedded
  python3 c9d_slides_build.py deck.md deck.html --artifact          # fragment for the Artifact tool
  python3 c9d_slides_build.py deck.md deck.html --check shots/ --sheet sheet.png --pdf deck.pdf
  python3 c9d_slides_build.py deck.md deck.html --no-embed          # Google Fonts link, drafts only

Tokens: palettes, the attribution line and the typeface names are read from the brand repo's
        tokens.json (--tokens PATH, $C9D_TOKENS, the repo copy when run from generators/,
        ./tokens.json beside this script, or fetched from github.com/C9D-Consulting/brand).
        Nothing is compiled in; without tokens.json the build stops.
Fonts:  Inter Tight, JetBrains Mono and Instrument Serif italic (all SIL OFL) are fetched from
        Google Fonts on first run, latin and latin-ext subsets, and cached as base64 @font-face
        rules in ./fonts/c9d-slides-fonts.css beside this script.
Needs:  the standard library to build. --check and --pdf need Playwright for Python with
        Chromium; --sheet also needs Pillow.

Exit status 1 when a lint or render check fails, so a deck is never delivered past a failure.
The c9d-consulting-slides skill carries this script verbatim; this file is the source of record.
"""
import argparse, base64, html, json, os, pathlib, re, sys, urllib.request

VERSION = "1.1"
HERE = pathlib.Path(__file__).resolve().parent
FONT_CACHE = HERE / "fonts" / "c9d-slides-fonts.css"
FONT_URL = ("https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300..600"
            "&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400..600&display=swap")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

TOKENS_URL = ("https://raw.githubusercontent.com/C9D-Consulting/brand/main/"
              "c9d-consulting-brand/assets/tokens.json")
BRAND = {}  # filled by load_tokens(): css variables per mode, attribution, families

REQUIRED = ["file_id", "classification", "title", "subtitle", "prepared_for", "prepared_by", "version"]
CLASSIFICATIONS = {"OPERATING EVIDENCE", "REFERENCE DESIGN", "CLIENT CONFIDENTIAL", "INTERNAL DRAFT", "REFUSED"}
DEFAULT_CLOSE = "Operator, not observer."
CLOSER = "Coordinated, not improvised."

# Same lists as c9d_html_build.py: the locked refuse list fails, the derived watch list warns.
REFUSED = [r"\btransform(ation|ative|s|ed|ing)?\b", r"\bjourney\b", r"\binnovat(ive|ion)\b",
           r"\bempower(ment|s|ed|ing)?\b", r"\bAI maturity model\b", r"\bAI cent(er|re) of excellence\b"]
WATCH = [r"\bthought leader(ship)?\b", r"\bbest-in-class\b", r"\bworld-class\b", r"\bindustry-leading\b",
         r"\bsynerg(y|ies)\b", r"\bleverag(e|es|ed|ing)\b", r"\bbandwidth\b", r"\bcircle back\b",
         r"\btouch base\b", r"\bdigital transformation\b", r"\bAI strategy roadmap\b", r"\bfractional CTO\b",
         r"\bwatchers?\b"]

# --------------------------------------------------------------------------- tokens

def load_tokens(path=None, refresh=False):
    """Read tokens.json. Same resolution order as c9d_pdf_build.py; no fallback palette."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.join(here, "..", "c9d-consulting-brand", "assets", "tokens.json")
    cache = os.path.join(here, "tokens.json")
    cands = [path, os.environ.get("C9D_TOKENS"), repo, cache]
    src = next((c for c in cands if c and os.path.exists(c)), None)
    if src is None or refresh:
        try:
            data = urllib.request.urlopen(TOKENS_URL, timeout=20).read()
            open(cache, "wb").write(data); src = cache
        except Exception as e:
            if src is None:
                sys.exit(f"error: tokens.json not found and could not be fetched ({e}). "
                         "Pass --tokens path/to/c9d-consulting-brand/assets/tokens.json.")
    d = json.load(open(src, encoding="utf8"))

    def css_vars(mode):
        c = d["color"][mode]
        return ";".join(f"--{k}:{v['value']}" for grp in ("ground", "rule", "ink", "signal", "crit")
                        for k, v in c[grp].items())
    st = d["typography"]["stack"]
    fam = lambda k: f"'{st[k]['family']}',{st[k]['fallback']}"
    BRAND.update(source=src, dark=css_vars("dark"), light=css_vars("light"),
                 attribution=d["naming"]["founder"]["attribution"],
                 families=f"--sans:{fam('display')};--serif:{fam('italic-accent')};--mono:{fam('mono')}")
    return BRAND

# --------------------------------------------------------------------------- parse

def parse_front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        sys.exit("error: source must start with --- front matter ---")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        sys.exit("error: front matter missing " + ", ".join(missing))
    return meta, text[m.end():]


def parse_blocks(lines):
    """Turn the lines under one heading into blocks."""
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1; continue
        if s.startswith("```"):
            lang = s[3:].strip().lower(); buf = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            blocks.append(("fence", (lang, "\n".join(buf)))); i += 1; continue
        if s.startswith("#### "):
            blocks.append(("col", s[5:].strip())); i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows)); continue
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            blocks.append(("quote", " ".join(buf))); continue
        m = re.match(r"^!\[(.*?)\]\((.*?)\)$", s)
        if m:
            blocks.append(("image", (m.group(1), m.group(2)))); i += 1; continue
        if re.match(r"^(- |\d+\. )", s):
            ordered = bool(re.match(r"^\d+\. ", s)); items = []
            while i < len(lines) and re.match(r"^\s*(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(- |\d+\. )", "", lines[i]).strip()); i += 1
            blocks.append(("ol" if ordered else "ul", items)); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^\s*(```|####|\||>|- |\d+\. |!\[)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        para = " ".join(buf)
        if para.startswith("Notes:"):
            blocks.append(("notes", para[6:].strip()))
        else:
            blocks.append(("p", para))
    return blocks


def split_heading(text):
    layout = None
    m = re.search(r"\s*\{(claim|compare|table|diagram|quote)\}\s*$", text)
    if m:
        layout, text = m.group(1), text[:m.start()]
    if " · " in text:
        eyebrow, title = text.split(" · ", 1)
        return eyebrow.strip(), title.strip(), layout
    return "", text.strip(), layout


def parse_slides(body):
    slides, cur, section_no, section_marker = [], None, 0, "§ 00 · FILE"
    for ln in body.splitlines():
        if ln.strip() == "---":
            continue  # stray rules are ignored, never slide breaks
        if re.match(r"^# ", ln):
            continue  # deck title comes from front matter
        m2, m3 = re.match(r"^## (.+)", ln), re.match(r"^### (.+)", ln)
        if m2 or m3:
            if cur: slides.append(cur)
            eyebrow, title, layout = split_heading((m2 or m3).group(1))
            if m2:
                section_no += 1
                if re.fullmatch(r"\d+", eyebrow):
                    section_no = int(eyebrow); eyebrow = f"SECTION {section_no:02d}"
                elif not eyebrow:
                    eyebrow = f"SECTION {section_no:02d}"
                section_marker = f"§ {section_no:02d} · {title.upper()}"
                cur = {"kind": "divider", "eyebrow": eyebrow.upper(), "title": title, "lines": [], "marker": section_marker}
            else:
                cur = {"kind": "content", "eyebrow": eyebrow.upper(), "title": title, "layout": layout,
                       "lines": [], "marker": section_marker}
            continue
        if cur is not None:
            cur["lines"].append(ln)
    if cur: slides.append(cur)
    for s in slides:
        s["blocks"] = parse_blocks(s.pop("lines"))
        if s["kind"] == "content" and not s["layout"]:
            kinds = [b[0] for b in s["blocks"] if b[0] != "notes"]
            if kinds.count("col") >= 2: s["layout"] = "compare"
            elif "table" in kinds: s["layout"] = "table"
            elif "image" in kinds or any(b[0] == "fence" for b in s["blocks"]): s["layout"] = "diagram"
            elif kinds and all(k == "quote" for k in kinds): s["layout"] = "quote"
            else: s["layout"] = "claim"
    return slides

# --------------------------------------------------------------------------- render

def inline(t):
    t = html.escape(t, quote=False)
    codes = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)
    return t


STATUS = {"open": "st-open", "resolved": "st-resolved", "refused": "st-refused", "critical": "st-critical", "closed": "st-resolved"}


def render_table(rows):
    if not rows: return ""
    head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
    body = ""
    for r in rows[1:]:
        cells = ""
        for c in r:
            cls = STATUS.get(c.strip().lower())
            cells += f'<td class="{cls}">{inline(c)}</td>' if cls else f"<td>{inline(c)}</td>"
        body += f"<tr>{cells}</tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_flow(blocks, src_dir):
    out = []
    for kind, data in blocks:
        if kind == "p": out.append(f"<p>{inline(data)}</p>")
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in data) + "</ul>")
        elif kind == "ol": out.append("<ol>" + "".join(f"<li><span class=\"n\">{i+1:02d}.</span> {inline(x)}</li>" for i, x in enumerate(data)) + "</ol>")
        elif kind == "table": out.append(render_table(data))
        elif kind == "quote": out.append(f'<blockquote>{inline(data)}</blockquote>')
        elif kind == "fence":
            lang, code = data
            out.append(f'<div class="figure">{code}</div>' if lang == "svg" else f"<pre>{html.escape(code)}</pre>")
        elif kind == "image":
            cap, path = data
            p = (src_dir / path)
            mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(p.suffix.lower()[1:], "application/octet-stream")
            if p.exists():
                uri = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
            else:
                uri = path
                print(f"warn: image not found, left as link: {path}", file=sys.stderr)
            out.append(f'<figure class="figure"><img src="{uri}" alt="{html.escape(cap)}">'
                       + (f'<figcaption>{inline(cap)}</figcaption>' if cap else "") + "</figure>")
    return "\n".join(out)


def wordmark(cls=""):
    return f'<span class="wordmark {cls}"><span class="wm-c9d">C9D</span><span class="wm-rest">Consulting</span></span>'


def chrome_top(meta, marker, n, total):
    return (f'<header class="chrome top"><span class="mono">{html.escape(meta["file_id"])}</span>'
            f'<span class="class-stamp">{html.escape(meta["classification"].upper())}</span>'
            f'<span class="mono marker">{html.escape(marker)}</span>'
            f'<span class="mono pageno">{n:02d} / {total:02d}</span></header>')


def chrome_bottom():
    return (f'<footer class="chrome bottom">{wordmark()}<span class="attr">{html.escape(BRAND["attribution"])}</span>'
            f'<span class="mono">c9d.consulting</span></footer>')


def render_slide(s, meta, n, total, src_dir):
    notes = " ".join(inline(d) for k, d in s.get("blocks", []) if k == "notes")
    blocks = [b for b in s.get("blocks", []) if b[0] != "notes"]
    kind = s["kind"]
    notes_html = f'<aside class="notes">{notes}</aside>' if notes else ""

    if kind == "cover":
        by = meta["prepared_by"]; name = by.split(",")[0].strip()
        ver = meta["version"].split("·")
        date = ver[1].strip() if len(ver) > 1 else ""
        return (f'<section class="slide s-cover" data-n="{n}">'
                f'<div class="cover-id"><span class="mono lg">{html.escape(meta["file_id"])}</span>'
                f'<span class="class-stamp">{html.escape(meta["classification"].upper())}</span></div>'
                f'<div class="cover-main"><h1>{inline(meta["title"])}</h1><hr class="rule-b">'
                f'<p class="cover-sub">{inline(meta["subtitle"])}</p></div>'
                f'<div class="cover-by"><span class="mute">Prepared by</span><span>{html.escape(name)}</span>{wordmark("inline")}</div>'
                f'<div class="cover-ver mono"><span>{html.escape(date)}</span><span>{html.escape(ver[0].strip())}</span></div>'
                f'{notes_html}</section>')
    if kind == "close":
        line = meta.get("close_line") or DEFAULT_CLOSE
        return (f'<section class="slide s-close" data-n="{n}"><div class="close-main">'
                f'<p class="close-a">{inline(line)}</p><p class="close-b">{CLOSER}</p></div>'
                f'<div class="close-by">{wordmark("inline")}<span class="mute">{html.escape(BRAND["attribution"])}</span></div>'
                f'<div class="close-dom mono">c9d.consulting</div></section>')

    top, bottom = chrome_top(meta, s["marker"], n, total), chrome_bottom()
    if kind == "meta":
        rows = [("DOCUMENT", meta["title"]), ("PREPARED FOR", meta["prepared_for"]), ("PREPARED BY", meta["prepared_by"]),
                ("CLASSIFICATION", meta["classification"].title()), ("VERSION", meta["version"])]
        dl = "".join(f'<div class="mrow"><dt>{k}</dt><dd>{inline(v)}</dd></div>' for k, v in rows)
        body = f'<div class="meta-wrap"><dl class="meta">{dl}</dl></div>'
        return f'<section class="slide s-meta" data-n="{n}">{top}<div class="body">{body}</div>{bottom}</section>'
    if kind == "divider":
        desc = render_flow(blocks, src_dir)
        body = (f'<div class="div-main"><div class="eyebrow">{html.escape(s["eyebrow"])}</div>'
                f'<h2>{inline(s["title"])}</h2><hr class="rule-b"><div class="div-desc">{desc}</div></div>')
        return f'<section class="slide s-divider" data-n="{n}">{top}<div class="body">{body}</div>{bottom}{notes_html}</section>'

    lay = s["layout"]
    eb = f'<div class="eyebrow">{html.escape(s["eyebrow"])}</div>' if s["eyebrow"] else ""
    if lay == "quote":
        q = " ".join(d for k, d in blocks if k == "quote")
        attr = " · ".join(x for x in (s["eyebrow"], s["title"].upper()) if x)
        body = (f'<div class="q-main"><span class="q-mark">&ldquo;</span><p class="q-text">{inline(q)}</p>'
                f'<div class="eyebrow">{html.escape(attr)}</div></div>')
    elif lay == "compare":
        pre, cols, cur = [], [], None
        for b in blocks:
            if b[0] == "col": cur = [b[1], []]; cols.append(cur)
            elif cur is None: pre.append(b)
            else: cur[1].append(b)
        colhtml = "".join(f'<div class="col"><div class="col-h">{inline(h.upper())}</div>{render_flow(bs, src_dir)}</div>' for h, bs in cols)
        body = f'{eb}<h3 class="t-row">{inline(s["title"])}</h3>{render_flow(pre, src_dir)}<div class="cols n{len(cols)}">{colhtml}</div>'
    elif lay == "table":
        pre = [b for b in blocks if b[0] == "p"]
        rest = [b for b in blocks if b[0] != "p"]
        sub = "".join(f'<p class="t-sub">{inline(d)}</p>' for _, d in pre)
        body = f'{eb}<h3 class="t-row">{inline(s["title"])}</h3>{sub}<div class="t-wrap">{render_flow(rest, src_dir)}</div>'
    elif lay == "diagram":
        text = [b for b in blocks if b[0] in ("p", "ul", "ol")]
        fig = [b for b in blocks if b[0] not in ("p", "ul", "ol")]
        body = (f'{eb}<h3 class="t-row">{inline(s["title"])}</h3>'
                f'<div class="dg{" with-text" if text else ""}"><div class="dg-fig">{render_flow(fig, src_dir)}</div>'
                + (f'<div class="dg-text">{render_flow(text, src_dir)}</div>' if text else "") + "</div>")
    else:  # claim
        pull = ""
        if blocks and blocks[-1][0] == "quote":
            pull = f'<div class="pull">{inline(blocks[-1][1])}</div>'; blocks = blocks[:-1]
        body = (f'<div class="claim-grid"><div class="claim-main">{eb}<h3 class="claim">{inline(s["title"])}</h3>'
                f'<div class="flow">{render_flow(blocks, src_dir)}</div></div>{pull}</div>')
    return (f'<section class="slide s-content l-{lay}" data-n="{n}">{top}<div class="body">{body}</div>'
            f'{bottom}{notes_html}</section>')

# --------------------------------------------------------------------------- fonts

def font_css(embed):
    if not embed:
        return f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONT_URL}" rel="stylesheet">'
    if not FONT_CACHE.exists():
        req = urllib.request.Request(FONT_URL, headers={"User-Agent": UA})
        css = urllib.request.urlopen(req, timeout=30).read().decode()
        faces = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*\{.*?\})", css, re.S)
        keep = []
        for subset, face in faces:
            if subset not in ("latin", "latin-ext"):
                continue
            url = re.search(r"url\((.*?)\)", face).group(1)
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
            keep.append(face.replace(url, "data:font/woff2;base64," + base64.b64encode(data).decode()))
        FONT_CACHE.parent.mkdir(parents=True, exist_ok=True)
        FONT_CACHE.write_text("\n".join(keep))
    return "<style>" + FONT_CACHE.read_text() + "</style>"

# --------------------------------------------------------------------------- page

CSS = r"""
:root{--mx:72px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--ink);overflow:hidden}
body{font-family:var(--sans);-webkit-font-smoothing:antialiased;font-feature-settings:'ss01','cv11'}
#viewport{position:fixed;inset:0;display:grid;place-items:center;background:var(--bg)}
#stage{width:1920px;height:1080px;position:relative;transform-origin:center center;flex:none}
.slide{position:absolute;inset:0;background:var(--bg);display:none;flex-direction:column;overflow:hidden}
.slide.on{display:flex}
.mono{font-family:var(--mono);font-size:18px;color:var(--ink-mute);letter-spacing:.04em}
.mono.lg{font-size:22px}
.mute{color:var(--ink-mute)}
.class-stamp{font-family:var(--sans);font-weight:500;font-size:16px;letter-spacing:.18em;text-transform:uppercase;color:var(--stamp)}
.eyebrow{font-family:var(--mono);font-weight:600;font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:var(--stamp-dim);margin-bottom:24px}
.wordmark{font-family:var(--sans);font-weight:400;letter-spacing:-.04em;color:var(--ink-bright);font-size:24px;white-space:nowrap}
.wm-c9d{color:var(--stamp)}.wm-rest{margin-left:.19em}
hr.rule-b{border:0;height:2px;background:var(--rule-bright)}
/* chrome */
.chrome{height:58px;flex:none;display:grid;align-items:center;padding:0 var(--mx);gap:32px}
.chrome.top{grid-template-columns:1fr 1.2fr 1.6fr .6fr;border-bottom:1px solid var(--rule)}
.chrome.top .marker{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chrome.top .pageno{text-align:right}
.chrome.bottom{grid-template-columns:1fr auto 1fr;border-top:1px solid var(--rule)}
.chrome.bottom .attr{font-size:18px;color:var(--ink-mute);text-align:center}
.chrome.bottom .mono{text-align:right}
.body{flex:1;min-height:0;padding:64px var(--mx) 48px;display:flex;flex-direction:column;position:relative}
/* type */
p,li{font-size:32px;line-height:1.5;color:var(--ink);max-width:40em}
.flow p+p,.flow p+ul,.flow ul+p,.flow p+ol,.flow ol+p{margin-top:28px}
strong{font-weight:600;color:var(--ink-bright)}
em{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--ink-bright);font-size:1.12em;line-height:1}
code{font-family:var(--mono);font-size:.82em;color:var(--ink-bright);letter-spacing:.02em}
a{color:var(--stamp);text-decoration:none;border-bottom:1px solid var(--stamp-dim)}
.ph{color:var(--stamp)}
ul,ol{list-style:none}
ul li{padding-left:1.1em;position:relative}ul li::before{content:"\2013";position:absolute;left:0;color:var(--stamp-dim)}
li+li{margin-top:14px}
ol .n{font-family:var(--mono);font-size:.7em;color:var(--stamp);margin-right:.5em;letter-spacing:.04em}
/* S-01 cover */
.s-cover{padding:86px}
.cover-id{display:flex;flex-direction:column;gap:10px}
.cover-main{flex:1;display:flex;flex-direction:column;justify-content:center}
.cover-main h1{font-weight:300;font-size:112px;line-height:1.05;letter-spacing:-.04em;color:var(--ink-bright);max-width:15em}
.cover-main hr{width:592px;margin:58px 0 44px}
.cover-sub{font-size:44px;font-weight:350;color:var(--ink-mute);line-height:1.25;max-width:none}
.cover-by{position:absolute;left:86px;bottom:86px;display:flex;flex-direction:column;gap:4px;font-size:24px;color:var(--ink-bright)}
.cover-by .wordmark{font-size:24px;letter-spacing:-.02em}
.cover-ver{position:absolute;right:86px;bottom:86px;display:flex;flex-direction:column;gap:6px;text-align:right;font-size:20px}
/* S-02 meta */
.meta-wrap{flex:1;display:flex;align-items:center;justify-content:center}
.meta{width:1184px;border-top:1px solid var(--rule-bright)}
.mrow{display:grid;grid-template-columns:340px 1fr;gap:32px;padding:26px 0;border-bottom:1px solid var(--rule);align-items:baseline}
.mrow dt{font-family:var(--mono);font-size:22px;letter-spacing:.18em;color:var(--stamp-dim);font-weight:600}
.mrow dd{font-size:28px;color:var(--ink-bright)}
/* S-03 divider */
.s-divider,.s-divider .chrome{background:var(--bg-2)}
.div-main{flex:1;display:flex;flex-direction:column;justify-content:center;padding-left:160px;max-width:1300px}
.div-main .eyebrow{font-size:24px;margin-bottom:44px}
.div-main h2{font-weight:300;font-size:96px;line-height:1.05;letter-spacing:-.04em;color:var(--ink-bright)}
.div-main hr{width:440px;margin:58px 0 44px}
.div-desc p{font-size:36px;color:var(--ink-mute);line-height:1.4}
/* S-04a claim */
.claim-grid{flex:1;display:grid;grid-template-columns:8fr 4fr;gap:72px;min-height:0}
.claim{font-weight:300;font-size:64px;line-height:1.12;letter-spacing:-.03em;color:var(--ink-bright);max-width:22em;margin-bottom:64px}
.pull{align-self:center;font-family:var(--serif);font-style:italic;font-size:48px;line-height:1.15;color:var(--stamp);border-left:2px solid var(--stamp-dim);padding-left:36px}
/* S-04b/c/d title row */
.t-row{font-weight:300;font-size:52px;line-height:1.12;letter-spacing:-.03em;color:var(--ink-bright);margin-bottom:20px}
.t-sub{font-size:26px;color:var(--ink-mute);margin-bottom:8px}
.cols{flex:1;display:grid;gap:0;margin-top:44px;min-height:0}
.cols.n2{grid-template-columns:1fr 1fr}.cols.n3{grid-template-columns:1fr 1fr 1fr}
.col{padding:0 56px;border-left:1px solid var(--rule)}.col:first-child{padding-left:0;border-left:0}
.col-h{font-family:var(--mono);font-size:20px;font-weight:600;letter-spacing:.18em;color:var(--stamp);margin-bottom:28px}
.col p,.col li{font-size:28px}.col p+p,.col p+ul,.col ul+p{margin-top:22px}
/* tables */
.t-wrap{margin-top:40px}
table{width:100%;border-collapse:collapse}
th{font-family:var(--mono);font-size:20px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--stamp-dim);text-align:left;padding:0 24px 18px 0;border-bottom:1px solid var(--rule-bright)}
td{font-size:26px;line-height:1.4;color:var(--ink);padding:18px 24px 18px 0;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
td.st-open,td.st-resolved,td.st-refused,td.st-critical{font-family:var(--mono);font-size:20px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;padding-top:22px}
td.st-open{color:var(--stamp)}td.st-resolved{color:var(--ink-mute)}td.st-refused,td.st-critical{color:var(--classified)}
/* S-04d diagram */
.dg{flex:1;display:grid;grid-template-columns:1fr;gap:72px;min-height:0;margin-top:32px}
.dg.with-text{grid-template-columns:8fr 4fr}
.dg-fig{min-height:0;display:flex;align-items:center;justify-content:center}
.figure{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.figure svg{width:100%;height:auto;max-height:100%}.figure img{max-width:100%;max-height:100%;min-height:0;object-fit:contain}
figcaption{font-family:var(--mono);font-size:18px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-mute)}
.dg-text{align-self:center;border-left:1px solid var(--rule);padding-left:48px}.dg-text p,.dg-text li{font-size:28px}
.dx-line{fill:none;stroke:var(--rule-bright);stroke-width:2}.dx-key{fill:none;stroke:var(--stamp);stroke-width:2}
.dx-label{fill:var(--ink-mute);font-family:var(--mono);letter-spacing:.18em}.dx-accent{fill:var(--stamp)}
.dx-text{fill:var(--ink-bright);font-family:var(--sans)}.dx-fill{fill:var(--bg-2)}
pre{font-family:var(--mono);font-size:22px;color:var(--ink);background:var(--bg-3);border:1px solid var(--rule);padding:28px;white-space:pre-wrap}
/* S-04e quote */
.q-main{flex:1;display:flex;flex-direction:column;justify-content:center;margin:0 auto;width:1184px;position:relative}
.q-mark{font-family:var(--serif);font-style:italic;font-size:176px;line-height:1;color:var(--stamp-dim);position:absolute;left:-110px;top:calc(50% - 190px)}
.q-text{font-weight:300;font-size:56px;line-height:1.22;letter-spacing:-.02em;color:var(--ink-bright);max-width:none;margin-bottom:58px}
.q-main .eyebrow{margin:0}
/* S-05 close */
.s-close{padding:86px}
.close-main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:44px}
.close-a,.close-b{font-weight:300;font-size:64px;letter-spacing:-.03em;line-height:1.1;max-width:none}
.close-a{color:var(--ink-bright)}.close-b{color:var(--stamp)}
.close-by{display:flex;flex-direction:column;gap:8px;font-size:22px}
.close-by .wordmark{font-size:40px}
.close-dom{position:absolute;right:86px;bottom:86px;font-size:20px}
/* notes + nav */
.notes{display:none}
#notes-panel{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:var(--bg-3);border-top:1px solid var(--rule-bright);
 padding:16px 24px;font-size:15px;line-height:1.5;color:var(--ink);display:none;z-index:5}
#notes-panel.on{display:block}
#notes-panel .k{font-family:var(--mono);font-size:11px;letter-spacing:.18em;color:var(--stamp-dim);display:block;margin-bottom:6px}
#progress{position:fixed;left:0;bottom:0;height:2px;background:var(--stamp-dim);transition:width .2s;z-index:4}
@media print{
 @page{size:1920px 1080px;margin:0}
 html,body{height:auto;overflow:visible;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 #viewport{position:static;display:block}#stage{transform:none!important;width:auto;height:auto}
 .slide{position:relative;display:flex!important;width:1920px;height:1080px;break-after:page;page-break-after:always}
 #notes-panel,#progress{display:none!important}
}
"""

JS = r"""
(function(){
 var slides=[].slice.call(document.querySelectorAll('.slide')),i=0,stage=document.getElementById('stage'),
     np=document.getElementById('notes-panel'),bar=document.getElementById('progress');
 function fit(){var s=Math.min(innerWidth/1920,innerHeight/1080);stage.style.transform='scale('+s+')';}
 function show(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach(function(s,k){s.classList.toggle('on',k===i)});
  var nt=slides[i].querySelector('.notes');np.innerHTML='<span class="k">NOTES · '+(i+1)+' / '+slides.length+'</span>'+(nt?nt.innerHTML:'<span class="k">NONE</span>');
  bar.style.width=((i+1)/slides.length*100)+'%';try{history.replaceState(null,'','#'+(i+1));}catch(e){}}
 addEventListener('keydown',function(e){var k=e.key;
  if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='ArrowDown'){e.preventDefault();show(i+1);}
  else if(k==='ArrowLeft'||k==='PageUp'||k==='ArrowUp'){e.preventDefault();show(i-1);}
  else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);
  else if(k==='n'||k==='N')np.classList.toggle('on');
  else if(k==='f'||k==='F'){if(document.fullscreenElement)document.exitFullscreen();else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();}});
 var x0=null;addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
 addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)show(i+(d<0?1:-1));x0=null},{passive:true});
 addEventListener('click',function(e){if(e.target.closest('a,#notes-panel'))return;if(getSelection&&String(getSelection()))return;show(i+(e.clientX>innerWidth/2?1:-1));});
 addEventListener('resize',fit);fit();window.__deck={show:show};
 var h=parseInt((location.hash||'').slice(1),10);show(isNaN(h)?0:h-1);
})();
"""


def build(src, embed, artifact):
    text = pathlib.Path(src).read_text()
    meta, body = parse_front(text)
    slides = [{"kind": "cover"}, {"kind": "meta", "marker": "§ 00 · FILE"}] + parse_slides(body) + [{"kind": "close"}]
    total = len(slides)
    src_dir = pathlib.Path(src).resolve().parent
    sections = "\n".join(render_slide(s, meta, n + 1, total, src_dir) for n, s in enumerate(slides))
    mode = "light" if meta.get("mode", "dark").lower() == "light" else "dark"
    title = f'{html.escape(meta["title"])} · C9D Consulting'
    tokens = f':root{{{BRAND[mode]};{BRAND["families"]}}}'  # one mode per deck, from tokens.json
    page = (f'<title>{title}</title>\n<meta name="description" content="{html.escape(meta["subtitle"])}">\n'
            f'{font_css(embed)}\n<style>{tokens}{CSS}</style>\n'
            f'<div id="viewport"><div id="stage">\n{sections}\n</div></div>\n'
            f'<div id="notes-panel"></div><div id="progress"></div>\n<script>{JS}</script>\n')
    if not artifact:
        page = (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
                f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                f'<meta name="generator" content="c9d_slides_build.py v{VERSION}">\n</head>\n<body>\n{page}</body>\n</html>\n')
    return meta, slides, page

# --------------------------------------------------------------------------- lint

def lint(meta, slides, src_text, page):
    """Returns (failures, warnings)."""
    probs, warns = [], []
    body = src_text.split("---", 2)[-1]
    prose = body + "\n" + meta["title"] + "\n" + meta["subtitle"]
    if "\u2014" in src_text: probs.append(f"voice: {src_text.count(chr(0x2014))} em-dash(es) in source")
    bare = [m for m in re.finditer(r"\bC9D\b(?! Consulting)(?!-)", prose)]
    for m in bare:
        probs.append(f"voice: bare 'C9D' near {prose[max(0,m.start()-30):m.end()+20]!r}")
    for pat in REFUSED:
        hits = re.findall(pat, prose, re.I)
        if hits: probs.append(f"voice: refused vocabulary /{pat}/ ({len(hits)})")
    for pat in WATCH:
        if re.search(pat, prose, re.I): warns.append(f"voice: watch-list term /{pat}/ (derived list, confirm intent)")
    if meta["classification"].upper() not in CLASSIFICATIONS:
        probs.append(f"front matter: classification not in {sorted(CLASSIFICATIONS)}")
    if meta["classification"].upper() != "INTERNAL DRAFT":
        ph = [m.group(0) for m in re.finditer(r"(?<![!\]])\[[^\]]+\](?!\()", src_text)]
        if ph: probs.append(f"placeholders: {len(ph)} unresolved in a non-draft deck, e.g. {ph[0]}")
    if page.count(html.escape(BRAND["attribution"])) < 2:
        probs.append("chrome: attribution line missing")
    if len(meta["title"]) > 48: probs.append("cover: title over 48 characters (two lines max at 112px)")
    for s in slides:
        if s["kind"] not in ("content", "divider"): continue
        t = s["title"]
        if re.search(r"\b(thank you|questions\??)\b", t, re.I): probs.append(f"slide: refused slide {t!r} (the close slide carries the closer)")
        words = [w for w in re.findall(r"[A-Za-z][\w'-]*", t)]
        caps = [w for w in words[1:] if w[0].isupper() and not w.isupper() and w not in ("C9D", "Consulting", "Brandon", "Wilburn")]
        if len(words) >= 4 and len(caps) >= max(2, len(words[1:]) * 0.6): probs.append(f"slide: title case, use sentence case: {t!r}")
        for k, d in s["blocks"]:
            if k in ("ul", "ol") and len(d) > 4: probs.append(f"slide: {len(d)} list items on {t!r} (4 max; use prose or a table)")
        if s.get("layout") == "claim":
            if len(t) > 90: probs.append(f"slide: claim over 90 characters (two lines max): {t!r}")
            if s["blocks"] and s["blocks"][-1][0] == "quote" and len(s["blocks"][-1][1].split()) > 8:
                probs.append(f"slide: pullquote over 8 words on {t!r}")
        if s.get("layout") == "table":
            rows = next((d for k, d in s["blocks"] if k == "table"), [])
            if len(rows) > 8: probs.append(f"slide: table on {t!r} has {len(rows)-1} rows (7 max; split the slide)")
    return probs, warns

# --------------------------------------------------------------------------- render checks

def contact_sheet(shots, out):
    from PIL import Image
    files = sorted(pathlib.Path(shots).glob("slide-*.png"))
    w, h, cols = 640, 360, 2
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols + 24 * (cols + 1), h * rows + 24 * (rows + 1)), "#2a2620")
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((w, h))
        sheet.paste(im, (24 + (i % cols) * (w + 24), 24 + (i // cols) * (h + 24)))
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)


def check(html_path, shots, pdf):
    from playwright.sync_api import sync_playwright
    probs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(pathlib.Path(html_path).resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        fonts = pg.evaluate("""async () => { const miss=[];
            for (const f of ['300 40px "Inter Tight"','600 20px "Inter Tight"','400 20px "JetBrains Mono"','italic 400 40px "Instrument Serif"']) {
              const got = await document.fonts.load(f); if (!got.length) miss.push(f); }
            return miss; }""")
        probs += [f"font not loaded: {f}" for f in fonts]
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        if shots: pathlib.Path(shots).mkdir(parents=True, exist_ok=True)
        for k in range(n):
            pg.evaluate(f"__deck.show({k})")
            res = pg.evaluate("""() => {
              const s=document.querySelector('.slide.on'), out=[];
              const b=s.querySelector('.body'); const lim=(b||s).getBoundingClientRect();
              s.querySelectorAll('.body *, .cover-main *, .close-main *').forEach(el=>{
                const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
                if(r.bottom>lim.bottom+1||r.right>lim.right+1) out.push(el.tagName.toLowerCase()+'.'+el.className);
              });
              const h=s.querySelector('.claim,.cover-main h1');
              if(h){const lh=parseFloat(getComputedStyle(h).lineHeight); if(h.getBoundingClientRect().height>lh*2.2) out.push('title runs past two lines');}
              s.querySelectorAll('th').forEach(th=>{const lh=parseFloat(getComputedStyle(th).lineHeight)||24; if(th.getBoundingClientRect().height>lh*1.9+18) out.push('table header wraps: '+th.textContent)});
              return [...new Set(out)].slice(0,4);}""")
            if res: probs.append(f"slide {k+1}: " + "; ".join(res))
            if shots: pg.screenshot(path=str(pathlib.Path(shots) / f"slide-{k+1:02d}.png"))
        if pdf:
            pg.pdf(path=pdf, width="1920px", height="1080px", print_background=True, prefer_css_page_size=True)
        b.close()
    return probs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source"); ap.add_argument("output")
    ap.add_argument("--artifact", action="store_true", help="omit doctype/html/head/body, for the Artifact tool")
    ap.add_argument("--no-embed", action="store_true", help="link Google Fonts instead of embedding (drafts only)")
    ap.add_argument("--check", metavar="SHOTS_DIR", help="render every slide, check overflow and fonts, save PNGs")
    ap.add_argument("--sheet", metavar="PNG", help="with --check, also write a two-up contact sheet")
    ap.add_argument("--pdf", metavar="PDF", help="also export a 16:9 PDF, one slide per page")
    ap.add_argument("--tokens", help="path to tokens.json (default: the repo copy, beside the script, else fetched)")
    ap.add_argument("--refresh-tokens", action="store_true", help="re-fetch tokens.json from the brand repo")
    a = ap.parse_args()
    load_tokens(a.tokens, a.refresh_tokens)
    meta, slides, page = build(a.source, not a.no_embed, a.artifact)
    pathlib.Path(a.output).write_text(page, encoding="utf-8")
    probs, warns = lint(meta, slides, pathlib.Path(a.source).read_text(encoding="utf-8"), page)
    print(f"built {a.output}: {len(slides)} slides, {len(page)//1024} KB, "
          f"{'artifact fragment' if a.artifact else 'standalone'}, tokens {BRAND['source']}")
    if a.check or a.pdf:
        target = a.output
        if a.artifact:  # checks need a full page
            _, _, full = build(a.source, not a.no_embed, False)
            target = str(pathlib.Path(a.output).with_suffix(".check.html"))
            pathlib.Path(target).write_text(full, encoding="utf-8")
        probs += check(target, a.check, a.pdf)
        if a.check and a.sheet:
            contact_sheet(a.check, a.sheet); print(f"sheet {a.sheet}")
        if a.pdf: print(f"pdf {a.pdf}")
    for w in warns: print("WARN ", w)
    for p in probs: print("FAIL ", p)
    if not probs: print("PASS  voice, placeholders, chrome" + (", render" if a.check or a.pdf else ""))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
