#!/usr/bin/env python3
"""C9D Consulting HTML build (The Dossier, screen mode).

Markdown with the C9D Consulting front matter in, one branded HTML page out.
Same source dialect as c9d_docx_build.py, so one .md builds both files.

  python3 c9d_html_build.py build  source.md output.html            # standalone page
  python3 c9d_html_build.py build  source.md output.html --artifact # fragment for the Artifact tool
  python3 c9d_html_build.py check  source.md output.html [--draft]  # parity + voice checks

No dependencies beyond the Python 3 standard library.
"""
import html
import re
import sys
from collections import Counter
from datetime import date

VERSION = "1.1"

REQUIRED_KEYS = ["file_id", "classification", "title", "subtitle",
                 "prepared_for", "prepared_by", "version", "section_marker"]
CLASSIFICATIONS = {"OPERATING EVIDENCE", "CLIENT CONFIDENTIAL", "INTERNAL DRAFT", "REFUSED"}

FONTS_HREF = ("https://fonts.googleapis.com/css2?family=Inter+Tight:wght@200..600"
              "&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400..600&display=swap")

CSS = r"""
:root{
  --bg:#0c0b08;--bg-2:#131210;--bg-3:#1a1815;--paper:#161410;
  --rule:#2a2620;--rule-bright:#3d362c;
  --ink-bright:#f0e6d0;--ink:#d8cdb8;--ink-mute:#8a7e6a;--ink-dim:#5a5042;
  --stamp:#d6743a;--stamp-dim:#8a4824;--classified:#c0392b;
  --space-1:4px;--space-2:8px;--space-3:16px;--space-4:24px;--space-5:32px;
  --space-6:48px;--space-7:64px;--space-8:96px;--space-9:128px;
  --font-display:'Inter Tight',Inter,-apple-system,system-ui,sans-serif;
  --font-italic:'Instrument Serif',Georgia,serif;
  --font-mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --track-eyebrow:0.18em;
  color-scheme:dark;
}
:root[data-mode="light"],:root[data-theme="light"],.light-mode{
  --bg:#f5f1e8;--bg-2:#ebe5d6;--bg-3:#e0d8c5;--paper:#ede7d4;
  --rule:#c8bda5;--rule-bright:#a89c82;
  --ink-bright:#1a1612;--ink:#2e2820;--ink-mute:#5a5042;--ink-dim:#8a7e6a;
  --stamp:#9c4f24;--stamp-dim:#6b3818;--classified:#8b2a20;
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--ink)}
body{font-family:var(--font-display);font-size:17px;line-height:1.6;font-weight:400;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  font-feature-settings:'ss01','cv11';min-height:100vh;overflow-x:hidden}
a{color:var(--stamp);text-decoration:none;border-bottom:1px solid var(--stamp-dim)}
a:hover{border-bottom-color:var(--stamp)}
strong{font-weight:600;color:var(--ink-bright)}
em{font-family:var(--font-italic);font-style:italic;font-weight:400;font-size:1.08em;color:var(--ink-bright)}
code{font-family:var(--font-mono);font-size:.84em;letter-spacing:.02em;color:var(--ink-bright)}
.mono{font-family:var(--font-mono);font-size:11px;letter-spacing:.04em;color:var(--ink-mute)}
.stamp{font-family:var(--font-mono);font-weight:600;font-size:11px;text-transform:uppercase;
  letter-spacing:var(--track-eyebrow);color:var(--stamp)}
.stamp--refused{color:var(--classified)}
.ph{color:var(--stamp)}
.wordmark{font-family:var(--font-display);font-weight:400;letter-spacing:-0.04em;color:var(--ink-bright)}
.wordmark__c9d{color:var(--stamp)}

.shell{max-width:1200px;margin:0 auto;padding:0 var(--space-6)}

/* chrome */
.chrome{display:grid;grid-template-columns:1fr auto 1fr;gap:var(--space-3);align-items:center;
  padding:var(--space-3) 0;border-bottom:1px solid var(--rule)}
.chrome > span{white-space:nowrap}
.chrome__c{text-align:center}.chrome__r{text-align:right}

/* cover */
.cover{padding:var(--space-9) 0 var(--space-8);border-bottom:1px solid var(--rule)}
.cover__eyebrow{margin-bottom:var(--space-6)}
.cover__title{font-size:clamp(40px,6vw,72px);font-weight:300;letter-spacing:-0.04em;line-height:1.05;
  color:var(--ink-bright);max-width:16ch;text-wrap:balance}
.cover__rule{border:0;height:1px;background:var(--rule-bright);width:240px;margin:var(--space-5) 0}
.cover__subtitle{font-size:22px;font-weight:300;line-height:1.4;color:var(--ink);max-width:40ch}
.meta{margin-top:var(--space-7);max-width:720px;border-top:1px solid var(--rule)}
.meta__row{display:grid;grid-template-columns:180px 1fr;gap:var(--space-4);padding:var(--space-2) 0;
  border-bottom:1px solid var(--rule);align-items:baseline}
.meta__row dt{font-family:var(--font-mono);font-size:10px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--track-eyebrow);color:var(--stamp)}
.meta__row dd{color:var(--ink)}
.meta__row dd.mono{font-size:13px;color:var(--ink)}

/* body: 5:7 asymmetric, rail carries the contents in mono */
.doc{display:grid;grid-template-columns:5fr 7fr;gap:var(--space-6);padding:var(--space-8) 0}
.rail{position:relative}
.toc{position:sticky;top:var(--space-5);border-top:1px solid var(--rule)}
.toc__label{display:block;padding:var(--space-3) 0 var(--space-2)}
.toc ol{list-style:none}
.toc li{border-bottom:1px solid var(--rule)}
.toc a{display:grid;grid-template-columns:92px 1fr;gap:var(--space-2);padding:var(--space-2) 0;border:0;
  color:var(--ink-mute);font-size:14px;line-height:1.35}
.toc a:hover{color:var(--ink-bright)}
.toc a .mono{font-size:10px;letter-spacing:.12em;color:var(--stamp);padding-top:2px}
.prose{min-width:0}
/* 28em holds the 65-character measure for Inter Tight at 17px; tables and headings may run wider */
.prose p,.prose ul,.prose ol{max-width:28em}
.lede{font-size:19px;font-weight:300;color:var(--ink-mute);margin-bottom:var(--space-6)}
.prose > p,.prose section > p{margin-bottom:var(--space-4)}
.section{padding-top:var(--space-7);scroll-margin-top:var(--space-4)}
.section:first-of-type{padding-top:0}
.section__eyebrow{display:block;margin-bottom:var(--space-3)}
.section h2{font-size:clamp(30px,3.4vw,40px);font-weight:300;letter-spacing:-0.03em;line-height:1.1;
  color:var(--ink-bright);text-wrap:balance}
.section__rule{border:0;height:1px;background:var(--rule-bright);margin:var(--space-4) 0 var(--space-5)}
.prose h3{font-size:24px;font-weight:300;letter-spacing:-0.02em;line-height:1.2;color:var(--ink-bright);
  margin:var(--space-6) 0 var(--space-3)}
.prose h4{font-size:18px;font-weight:500;letter-spacing:-0.01em;color:var(--ink-bright);
  margin:var(--space-5) 0 var(--space-2)}
.prose ul,.prose ol{list-style:none;margin:0 0 var(--space-4)}
.prose li{position:relative;padding-left:var(--space-5);margin-bottom:var(--space-2)}
.prose ul > li::before{content:"\2013";position:absolute;left:0;color:var(--stamp)}
.prose ol{counter-reset:n}
.prose ol > li{counter-increment:n}
.prose ol > li::before{content:counter(n,decimal-leading-zero) ".";position:absolute;left:0;top:.25em;
  font-family:var(--font-mono);font-size:12px;color:var(--stamp)}
.sig{font-family:var(--font-mono);color:var(--ink-dim);letter-spacing:0}

/* tables: hairlines, mono caps header */
.table-wrap{margin:var(--space-4) 0 var(--space-5);overflow-x:auto;border-top:1px solid var(--rule-bright)}
table{width:100%;border-collapse:collapse}
th{font-family:var(--font-mono);font-size:10px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--track-eyebrow);color:var(--stamp);text-align:left;padding:var(--space-2) var(--space-3);
  background:var(--bg-2);border-bottom:1px solid var(--rule-bright);vertical-align:bottom}
td{padding:var(--space-2) var(--space-3);font-size:14px;line-height:1.5;color:var(--ink);
  border-bottom:1px solid var(--rule);vertical-align:top}
th:first-child,td:first-child{padding-left:0}
th:first-child{padding-left:var(--space-2)}
td:first-child{padding-left:var(--space-2)}
td.nw{white-space:nowrap}

/* footer */
.foot{border-top:1px solid var(--rule);padding:var(--space-7) 0 var(--space-7)}
.foot__brand{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--space-2) var(--space-3)}
.foot__brand .wordmark{font-size:18px}
.foot__attr{color:var(--ink-mute);font-size:13px}
.foot__meta{display:flex;flex-wrap:wrap;gap:var(--space-2) var(--space-5);margin-top:var(--space-3)}
.foot__closer{margin-top:var(--space-5);font-family:var(--font-italic);font-style:italic;font-size:22px;color:var(--stamp)}

@media (max-width:900px){
  .doc{grid-template-columns:1fr;gap:0;padding-top:var(--space-6)}
  .rail{display:none}
}
@media (max-width:720px){
  .shell{padding:0 16px}
  body{font-size:16px}
  .chrome{grid-template-columns:auto auto;justify-content:space-between}
  .chrome__c{display:none}
  .cover{padding:var(--space-7) 0 var(--space-6)}
  .cover__title{font-size:clamp(34px,9vw,52px)}
  .cover__subtitle{font-size:19px}
  .meta__row{grid-template-columns:1fr;gap:2px}
  td{font-size:13px}
}

@media print{
  @page{size:Letter;margin:1.3in 1in 1in}
  :root{
    --bg:#ffffff;--bg-2:#ebe5d6;--bg-3:#e0d8c5;--paper:#f8f4eb;
    --rule:#c8bda5;--rule-bright:#a89c82;
    --ink-bright:#1a1612;--ink:#2e2820;--ink-mute:#5a5042;--ink-dim:#8a7e6a;
    --stamp:#9c4f24;--stamp-dim:#6b3818;--classified:#8b2a20;color-scheme:light;
  }
  html,body{background:#fff!important}
  body{font-size:11pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .shell{max-width:none;padding:0}
  .cover{padding-top:1.4in;break-after:page;border:0}
  .chrome{grid-template-columns:auto auto auto;justify-content:space-between}
  .table-wrap.keep{break-inside:avoid}
  .doc{display:block;padding:0}
  .rail{display:none}
  .prose p,.prose ul,.prose ol{max-width:none}
  .section{break-before:auto;padding-top:28pt}
  .section h2,.prose h3,.prose h4{break-after:avoid}
  tr{break-inside:avoid}
  thead{display:table-header-group}
  .table-wrap{overflow:visible}
  a{border:0;color:inherit}
  .foot{break-inside:avoid;break-before:avoid;padding:18pt 0 0}
  .foot__closer{font-size:16pt}
}
"""

# ---------------------------------------------------------------- parsing

def parse_front_matter(text):
    if not text.startswith("---"):
        sys.exit("error: source has no YAML front matter")
    end = text.find("\n---", 3)
    if end < 0:
        sys.exit("error: front matter is not closed with ---")
    fm = {}
    for line in text[3:end].strip().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        fm[k.strip()] = v
    missing = [k for k in REQUIRED_KEYS if not fm.get(k)]
    if missing:
        sys.exit("error: front matter missing " + ", ".join(missing))
    fm["classification"] = fm["classification"].upper()
    if fm["classification"] not in CLASSIFICATIONS:
        sys.exit("error: classification must be one of " + ", ".join(sorted(CLASSIFICATIONS)))
    body = text[end + 4:].lstrip("\n")
    return fm, body


def slug(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "section"


def inline(s):
    """Escape, then apply the dialect's inline marks."""
    stash = []

    def keep(fragment):
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    s = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{html.escape(m.group(1))}</code>"), s)
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+|#[^)\s]*)\)",
               lambda m: keep(f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>'), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', s)
    s = re.sub(r"_{20,}", lambda m: f'<span class="sig">{m.group(0)}</span>', s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)
    return s


def eyebrow_for(label):
    label = label.strip()
    if re.fullmatch(r"\d+", label):
        return f"SECTION {int(label):02d}"
    return label.upper()


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def parse_body(md):
    """Return (lede, blocks html list, toc entries)."""
    lines = md.splitlines()
    out, toc = [], []
    lede = None
    i, n = 0, len(lines)
    in_section = False
    seen_ids = Counter()

    def close_section():
        nonlocal in_section
        if in_section:
            out.append("</section>")
            in_section = False

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            i += 1
            continue
        if s.startswith("# "):
            # Cover carries the title. A whole-line *description* right under it becomes the lede.
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i < n and re.fullmatch(r"\*[^*].*[^*]\*", lines[i].strip()):
                lede = inline(lines[i].strip()[1:-1])
                i += 1
            continue
        if s.startswith("## "):
            close_section()
            head = s[3:].strip()
            head = re.sub(r"^(\d+)\.\s+", r"\1 · ", head)
            if " · " in head:
                label, title = head.split(" · ", 1)
                eb = eyebrow_for(label)
            else:
                title, eb = head, "SECTION"
            sid = slug(title)
            seen_ids[sid] += 1
            if seen_ids[sid] > 1:
                sid = f"{sid}-{seen_ids[sid]}"
            toc.append((eb, inline(title), sid))
            out.append(f'<section class="section" id="{sid}">')
            out.append(f'<span class="section__eyebrow stamp">{html.escape(eb)}</span>')
            out.append(f"<h2>{inline(title)}</h2>")
            out.append('<hr class="section__rule">')
            in_section = True
            i += 1
            continue
        if s.startswith("#### "):
            out.append(f"<h4>{inline(s[5:])}</h4>"); i += 1; continue
        if s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>"); i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i]); i += 1
            header = split_row(rows[0])
            body_rows = [split_row(r) for r in rows[1:]
                         if not re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", r.strip())]
            keep = " keep" if len(body_rows) <= 8 else ""
            t = [f'<div class="table-wrap{keep}"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in header]
            t.append("</tr></thead><tbody>")
            for r in body_rows:
                r = r + [""] * (len(header) - len(r))
                cells = []
                for c in r[:len(header)]:
                    nw = ' class="nw"' if len(c) <= 12 and " " not in c else ""
                    cells.append(f"<td{nw}>{inline(c)}</td>")
                t.append("<tr>" + "".join(cells) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if re.match(r"[-*+]\s+", s):
            items = []
            while i < n and re.match(r"\s*[-*+]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*+]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"\d+[.)]\s+", s):
            items = []
            while i < n and re.match(r"\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        para = []
        while i < n and lines[i].strip() and not re.match(r"\s*(#{1,4} |\||[-*+]\s+|\d+[.)]\s+)", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    close_section()
    return lede, out, toc

# ---------------------------------------------------------------- render

def wordmark():
    return '<span class="wordmark"><span class="wordmark__c9d">C9D</span> Consulting</span>'


def render(fm, body_md, artifact=False):
    lede, blocks, toc = parse_body(body_md)
    esc = lambda k: html.escape(fm[k])
    stamp_cls = "stamp stamp--refused" if fm["classification"] == "REFUSED" else "stamp"
    mode = fm.get("mode", "dark").lower()
    year = date.today().year
    desc = html.escape(fm.get("description") or fm["subtitle"])

    toc_html = ""
    if len(toc) >= 2:
        toc_html = ('<nav class="toc" aria-label="Contents"><span class="toc__label stamp">Contents</span><ol>'
                    + "".join(f'<li><a href="#{sid}"><span class="mono">{html.escape(eb)}</span>'
                              f"<span>{t}</span></a></li>" for eb, t, sid in toc)
                    + "</ol></nav>")

    page = f"""<div class="page">
<div class="shell">
<header class="chrome" aria-label="Document chrome">
  <span class="chrome__l mono">{esc('file_id')}</span>
  <span class="chrome__c {stamp_cls}">{esc('classification')}</span>
  <span class="chrome__r mono">§ {esc('section_marker')} · {esc('version')}</span>
</header>
<section class="cover" aria-label="Cover">
  <div class="cover__eyebrow"><span class="{stamp_cls}">{esc('classification')}</span></div>
  <h1 class="cover__title">{esc('title')}</h1>
  <hr class="cover__rule">
  <p class="cover__subtitle">{inline(fm['subtitle'])}</p>
  <dl class="meta">
    <div class="meta__row"><dt>Prepared for</dt><dd>{esc('prepared_for')}</dd></div>
    <div class="meta__row"><dt>Prepared by</dt><dd>{esc('prepared_by')}</dd></div>
    <div class="meta__row"><dt>Version</dt><dd class="mono">{esc('version')}</dd></div>
    <div class="meta__row"><dt>File</dt><dd class="mono">{esc('file_id')}</dd></div>
  </dl>
</section>
<div class="doc">
  <aside class="rail">{toc_html}</aside>
  <main class="prose">
{('<p class="lede">' + lede + '</p>') if lede else ''}
{chr(10).join(blocks)}
  </main>
</div>
<footer class="foot">
  <div class="foot__brand">{wordmark()}<span class="foot__attr">A practice of Brandon Wilburn.</span></div>
  <div class="foot__meta"><span class="mono">c9d.consulting</span><span class="mono">© {year} C9D Consulting LLC</span><span class="mono">{esc('file_id')} · {esc('version')}</span></div>
  <div class="foot__closer">Coordinated, not improvised.</div>
</footer>
</div>
</div>"""

    title = f"{fm['title']} · C9D Consulting"
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             f'<link rel="stylesheet" href="{html.escape(FONTS_HREF)}">')
    mode_script = ('<script>document.documentElement.setAttribute("data-mode","light")</script>'
                   if mode == "light" else "")
    head_bits = (f"<title>{html.escape(title)}</title>\n"
                 f'<meta name="description" content="{desc}">\n'
                 f'<meta name="generator" content="c9d_html_build {VERSION}">\n'
                 f"{fonts}\n<style>{CSS}</style>")
    if artifact:
        # Artifact tool wraps the skeleton; no doctype/html/head/body here.
        return f"{head_bits}\n{mode_script}\n{page}\n"
    root_attr = ' data-mode="light"' if mode == "light" else ""
    return f"""<!doctype html>
<html lang="en"{root_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_bits}
</head>
<body>
{page}
</body>
</html>
"""

# ---------------------------------------------------------------- checks

REFUSED = [r"\btransform(ation|ative|s|ed|ing)?\b", r"\bjourney\b", r"\binnovat(ive|ion)\b",
           r"\bempower(ment|s|ed|ing)?\b", r"\bAI maturity model\b", r"\bAI cent(er|re) of excellence\b"]
WATCH = [r"\bthought leader(ship)?\b", r"\bbest-in-class\b", r"\bworld-class\b", r"\bindustry-leading\b",
         r"\bsynerg(y|ies)\b", r"\bleverag(e|es|ed|ing)\b", r"\bbandwidth\b", r"\bcircle back\b",
         r"\btouch base\b", r"\bdigital transformation\b", r"\bAI strategy roadmap\b", r"\bfractional CTO\b",
         r"\bwatchers?\b"]


def words(text):
    return Counter(w.lower() for w in re.findall(r"[A-Za-z0-9$%']+", text))


def html_text(h):
    h = re.sub(r"(?s)<(style|script|title)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<nav .*?</nav>", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return html.unescape(h)


def md_text(body):
    t = re.sub(r"(?m)^#\s+.*$", " ", body)            # title lives on the cover
    t = re.sub(r"(?m)^\s*\|?\s*:?-{2,}.*$", " ", t)   # table separators
    t = re.sub(r"\[([^\]]+)\]\((?:[^)]+)\)", r"\1", t)  # link targets
    t = re.sub(r"(?m)^\s*\d+[.)]\s+", " ", t)         # list numbers render as CSS counters
    t = re.sub(r"(?m)^(##\s+)\d+\s*[·.]\s+", r"\1", t)  # numeric section labels become SECTION 0N
    return t


def check(src, out_path, draft=False):
    text = open(src, encoding="utf-8").read()
    fm, body = parse_front_matter(text)
    h = open(out_path, encoding="utf-8").read()
    problems, warnings = [], []

    src_words = words(md_text(body))
    out_words = words(html_text(h))
    missing = src_words - out_words
    if missing:
        problems.append("parity: words in source missing from HTML: " + ", ".join(
            f"{w}×{c}" for w, c in missing.most_common(20)))

    prose = body + "\n" + fm["title"] + "\n" + fm["subtitle"]
    if "\u2014" in prose:
        problems.append(f"voice: {prose.count(chr(0x2014))} em-dash(es) in source")
    bare = [m.group(0) for m in re.finditer(r"\bC9D\b(?! Consulting)(?!-)", prose)]
    if bare:
        problems.append(f"voice: bare 'C9D' used {len(bare)} time(s); write 'C9D Consulting'")
    for pat in REFUSED:
        hits = re.findall(pat, prose, re.I)
        if hits:
            problems.append(f"voice: refused vocabulary /{pat}/ ({len(hits)})")
    for pat in WATCH:
        if re.search(pat, prose, re.I):
            warnings.append(f"voice: watch-list term /{pat}/ (derived list, confirm intent)")
    brackets = re.findall(r"(?<!\])\[[^\]]+\](?!\()", body)
    if brackets and not draft:
        problems.append(f"placeholders: {len(brackets)} unresolved [bracket](s), e.g. {brackets[0]}")
    if "A practice of Brandon Wilburn" not in h:
        problems.append("chrome: attribution line missing")
    if re.search(r"https?://(?!fonts\.googleapis\.com|fonts\.gstatic\.com)[^\"'\s)]+\.(js|css)\b", h):
        problems.append("self-contained: external script or stylesheet other than Google Fonts")
    title_lines = len(fm["title"])
    if title_lines > 48:
        warnings.append(f"cover: title is {title_lines} characters; aim for two lines (about 32)")

    for w in warnings:
        print("WARN ", w)
    for p in problems:
        print("FAIL ", p)
    if not problems:
        print("PASS  parity, voice, placeholders, chrome")
    return 1 if problems else 0

# ---------------------------------------------------------------- cli

def main(argv):
    if len(argv) < 4 or argv[1] not in ("build", "check"):
        print(__doc__)
        return 2
    cmd, src, dst = argv[1], argv[2], argv[3]
    if cmd == "check":
        return check(src, dst, draft="--draft" in argv)
    fm, body = parse_front_matter(open(src, encoding="utf-8").read())
    open(dst, "w", encoding="utf-8").write(render(fm, body, artifact="--artifact" in argv))
    print(f"built {dst} ({'artifact fragment' if '--artifact' in argv else 'standalone'})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
