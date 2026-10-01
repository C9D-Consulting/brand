#!/usr/bin/env python3
"""c9d_flyer_build.py: build a one-page C9D Consulting flyer or service sheet (The Dossier,
screen mode) from a markdown source with YAML front matter.

Usage:  python3 c9d_flyer_build.py source.md out.pdf [--verify] [--html]
Shares tokens, fonts, front matter parsing and the inline dialect with c9d_pdf_build.py,
which must sit beside this script. Layout is PROPOSED (templates/flyer-spec.md), not locked.

Front matter: the eight document keys (file_id, classification, title, subtitle,
prepared_for, prepared_by, version, section_marker) plus optional `eyebrow` (line above the
title) and `tagline` (footer, default "The playbook, not the deck.").

Body: `## EYEBROW · Title` opens a band. The band's layout follows from its content:
  brief   a table plus paragraphs: table renders as a key/value column (header row is a
          label, not rendered), paragraphs beside it under the Title as a heading
  strip   a table alone: each row becomes a numbered column (cells: name | window | work)
  split   two ### subsections: first narrow, second wide; ### text is the column eyebrow
  cards   #### `ID · Title` blocks, each with paragraphs, rendered as side-by-side cards
In split and cards bands the ## line is a structural label and is not rendered.
Inline: **bold**, *italic* (Instrument Serif), `mono` (renders as amber signal, use it for
measured figures only).
"""
import re, sys, os, html, subprocess, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9d_pdf_build as b

VERSION = "0.1"
E = html.escape

def inl(text):
    out = []
    for kind, t in b.inline_runs(text):
        t = E(t, quote=False)
        out.append({"bold": f"<b>{t}</b>", "italic": f"<em>{t}</em>",
                    "mono": f'<span class="sig">{t}</span>',
                    "placeholder": f'<span class="sig">{t}</span>'}.get(kind, t))
    return "".join(out)

def balance(title):
    """Two lines, split at the word boundary nearest the middle, for titles over 22 chars."""
    if len(title) <= 22: return E(title)
    words = title.split(); best = None
    for i in range(1, len(words)):
        a, c = " ".join(words[:i]), " ".join(words[i:])
        d = abs(len(a) - len(c))
        if best is None or d < best[0]: best = (d, a, c)
    return f"{E(best[1])}<br>{E(best[2])}"

def bands(blocks):
    out, cur = [], None
    for kind, val in blocks:
        if kind == "h2":
            cur = {"head": val, "blocks": []}; out.append(cur)
        elif cur is not None:
            cur["blocks"].append((kind, val))
        else:
            sys.exit(f"content before the first ## band: {kind} {val[:40]!r}")
    return out

def split_head(h):
    return h.split(" · ", 1) if " · " in h else (h, "")

def render_band(band, rendered):
    head = band["head"]; bl = band["blocks"]; kinds = [k for k, _ in bl]
    eyebrow, title = split_head(head)
    if "h4" in kinds:                                   # cards
        cards, cur = [], None
        for k, v in bl:
            if k == "h4": cur = [v, []]; cards.append(cur)
            elif k == "p" and cur: cur[1].append(v)
        html_ = '<div class="ext">'
        for h, ps in cards:
            cid, ct = split_head(h); rendered += [h] + ps
            html_ += (f'<div><div class="id">{E(cid)}</div><div class="t">{inl(ct)}</div>'
                      + "".join(f"<p>{inl(p)}</p>" for p in ps) + "</div>")
        return html_ + "</div>"
    if "h3" in kinds:                                   # split
        cols, cur = [], None
        for k, v in bl:
            if k == "h3": cur = [v, []]; cols.append(cur)
            elif cur: cur[1].append((k, v))
        if len(cols) != 2: sys.exit(f"split band '{head}' needs exactly two ### subsections")
        parts = []
        for (h, items), cls in zip(cols, ("side", "main")):
            rendered.append(h); inner = f'<div class="eyebrow">{E(h)}</div>'
            for k, v in items:
                if k == "ul":
                    inner += "<ul>" + "".join(f"<li>{inl(i)}</li>" for i in v) + "</ul>"; rendered += v
                elif k == "p":
                    inner += f"<p>{inl(v)}</p>"; rendered.append(v)
            parts.append(f'<div class="{cls}">{inner}</div>')
        return '<div class="rule"></div><div class="cols">' + "".join(parts) + "</div>"
    tables = [v for k, v in bl if k == "table"]; paras = [v for k, v in bl if k == "p"]
    if tables and not paras:                            # strip
        rows = tables[0][1:]; rendered.append(head)
        cells = "".join(
            f'<div class="ph"><div class="n">{i:02d}</div><div class="t">{inl(r[0])}</div>'
            f'<div class="w">{inl(r[1])}</div><p>{inl(r[2])}</p></div>'
            for i, r in enumerate(rows, 1))
        for r in rows: rendered += r[:3]
        return f'<div class="eyebrow gap">{E(head)}</div><div class="phases">{cells}</div>'
    if tables and paras:                                # brief
        rows = tables[0][1:]; rendered += [eyebrow, title] + paras
        for r in rows: rendered += r[:2]
        kv = "".join(f'<tr><td class="k">{inl(r[0])}</td><td class="v">{inl(r[1])}</td></tr>' for r in rows)
        prose = "".join(f"<p>{inl(p)}</p>" for p in paras)
        return (f'<div class="rule"></div><div class="eyebrow gap">{E(eyebrow)}</div><div class="cols tight">'
                f'<div class="side"><table class="kv">{kv}</table></div>'
                f'<div class="main"><h2>{inl(title)}</h2>{prose}</div></div>')
    sys.exit(f"band '{head}' matches no flyer layout (brief, strip, split, cards)")

def css(P):
    faces = "\n".join(
        f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};"
        f"src:url('file://{os.path.join(b.FONT_DIR, f)}');}}"
        for (fam, w, st), f in b.FONT_FILES.items())
    return faces + f"""
@page {{ size: Letter; margin: 0; background: {P['bg']}; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter Tight'; font-weight: 400; color: {P['ink']}; background: {P['bg']};
  font-size: 9.2pt; line-height: 1.42; }}
.page {{ display: flex; flex-direction: column; width: 8.5in; height: 11in; padding: 0.45in 0.6in 0.4in; }}
.meta {{ display: flex; border-top: 1px solid {P['rule']}; border-bottom: 1px solid {P['rule']};
  font-family: 'JetBrains Mono'; font-weight: 500; font-size: 6.6pt; letter-spacing: .12em;
  text-transform: uppercase; color: {P['ink_mute']}; }}
.meta div {{ padding: 5pt 8pt; border-right: 1px solid {P['rule']}; flex: 1; }}
.meta div:last-child {{ border-right: 0; text-align: right; }}
.meta .stamp {{ color: {P['stamp']}; }}
.eyebrow {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 7pt; letter-spacing: .18em;
  text-transform: uppercase; color: {P['stamp_dim']}; margin-bottom: 6pt; }}
.eyebrow.gap {{ margin-top: 8pt; }}
.hero {{ margin: 12pt 0 9pt; }}
h1 {{ font-weight: 300; font-size: 28pt; line-height: 1.03; letter-spacing: -0.03em;
  color: {P['ink_bright']}; margin-bottom: 7pt; }}
.lede {{ font-weight: 300; font-size: 11.5pt; line-height: 1.38; color: {P['ink']}; max-width: 6in; }}
em {{ font-family: 'Instrument Serif'; font-style: italic; color: {P['ink_bright']}; font-size: 1.12em; }}
b {{ font-weight: 600; color: {P['ink_bright']}; }}
.sig {{ color: {P['stamp']}; font-family: 'JetBrains Mono'; font-weight: 500; }}
.rule {{ border-top: 1px solid {P['rule']}; }}
.cols {{ display: flex; gap: 22pt; padding: 8pt 0; }}
.cols.tight {{ padding-top: 0; }}
.side {{ flex: 5; }} .main {{ flex: 7; }}
.kv {{ width: 100%; border-collapse: collapse; }}
.kv td {{ padding: 3pt 0; border-bottom: 1px solid {P['rule']}; vertical-align: top; }}
.kv td.k {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 6.6pt; letter-spacing: .12em;
  text-transform: uppercase; color: {P['ink_mute']}; width: 34%; padding-top: 4.2pt; }}
.kv td.v {{ color: {P['ink']}; font-size: 8.8pt; }}
h2 {{ font-weight: 400; font-size: 13pt; color: {P['ink_bright']}; letter-spacing: -0.01em; margin-bottom: 5pt; }}
p + p {{ margin-top: 6pt; }}
.phases {{ display: flex; border-top: 1px solid {P['rule_bright']}; border-bottom: 1px solid {P['rule']}; }}
.ph {{ flex: 1; padding: 6pt 10pt 8pt 0; border-right: 1px solid {P['rule']}; margin-right: 10pt; }}
.ph:last-child {{ border-right: 0; margin-right: 0; }}
.ph .n {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 7pt; letter-spacing: .14em; color: {P['stamp']}; }}
.ph .t {{ font-weight: 500; font-size: 10.5pt; color: {P['ink_bright']}; margin: 2pt 0 3pt; }}
.ph .w {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 6.4pt; letter-spacing: .1em; color: {P['ink_mute']}; text-transform: uppercase; margin-bottom: 4pt; }}
.ph p {{ font-size: 8.4pt; line-height: 1.45; }}
ul {{ list-style: none; }}
li {{ padding: 2.6pt 0 2.6pt 14pt; position: relative; border-bottom: 1px solid {P['rule']}; font-size: 8.8pt; }}
li:before {{ content: '\\2013'; position: absolute; left: 0; color: {P['stamp']}; }}
.ext {{ display: flex; gap: 22pt; padding: 4pt 0 6pt; }}
.ext > div {{ flex: 1; background: {P['bg2']}; border: 1px solid {P['rule']}; padding: 8pt 11pt; }}
.ext .id {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 6.6pt; letter-spacing: .14em; color: {P['stamp']}; text-transform: uppercase; }}
.ext .t {{ font-weight: 500; font-size: 10.5pt; color: {P['ink_bright']}; margin: 2pt 0 3pt; }}
.ext p {{ font-size: 8.4pt; line-height: 1.45; }}
.foot {{ margin-top: auto; display: flex; align-items: baseline; justify-content: space-between;
  border-top: 1px solid {P['rule']}; padding-top: 6pt; }}
.wm {{ font-weight: 400; letter-spacing: -0.04em; font-size: 14pt; color: {P['ink_bright']}; }}
.wm span {{ color: {P['stamp']}; }}
.attr {{ font-size: 8pt; color: {P['ink_mute']}; margin-left: 8pt; }}
.foot .r {{ font-family: 'JetBrains Mono'; font-weight: 500; font-size: 6.8pt; letter-spacing: .1em; color: {P['ink_mute']}; text-transform: uppercase; }}
.foot .r .stamp {{ color: {P['stamp']}; }}
"""

def build(meta, body):
    P = b.BRAND["palettes"]["screen"]; rendered = []
    tag = meta.get("tagline", "The playbook, not the deck.")
    content = "".join(render_band(bd, rendered) for bd in bands(b.parse_blocks(body)))
    rendered += [meta.get(k, "") for k in ("file_id", "classification", "section_marker",
                                           "version", "eyebrow", "title", "subtitle")] + [tag]
    page = f"""<div class="page">
 <div class="meta"><div>{E(meta['file_id'])}</div><div class="stamp">{E(meta['classification'])}</div>
  <div>§ {E(meta['section_marker'])}</div><div>{E(meta['version'])}</div></div>
 <div class="hero"><div class="eyebrow">{E(meta.get('eyebrow', ''))}</div>
  <h1>{balance(meta['title'])}</h1><p class="lede">{inl(meta['subtitle'])}</p></div>
 {content}
 <div class="foot"><div><span class="wm"><span>C9D</span> Consulting</span>
  <span class="attr">{E(b.BRAND['attribution'])}</span></div>
  <div class="r">{E(tag)} · <span class="stamp">c9d.consulting</span></div></div>
</div>"""
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{E(meta['title'])}</title>"
           f"<meta name='author' content='{E(meta.get('prepared_by', 'C9D Consulting'))}'>"
           f"<meta name='description' content='{E(re.sub(r'[*`]', '', meta['subtitle']))}'>"
           f"<meta name='keywords' content='{E(meta['section_marker'])}'>"
           f"<style>{css(P)}</style></head><body>{page}</body></html>")
    return doc, "\n".join(rendered)

def verify(pdf, rendered_src):
    ok = True
    fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    bad = [f for f in fonts if not re.search(r"Inter-?Tight|JetBrains-?Mono|Instrument-?Serif", f)
           or " yes " not in f]
    print("fonts:", ", ".join(sorted({re.sub(r'^[A-Z]{6}\+', '', f.split()[0]) for f in fonts})))
    if bad: ok = False; print("FAIL fonts not brand or not embedded:", bad)
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)); print("pages:", pages)
    if pages != 1: ok = False; print("FAIL a flyer is one page")
    raw = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    n = raw.count(b.BRAND["attribution"]); print(f"attribution x{n}")
    if n < 1: ok = False; print("FAIL attribution missing")
    # Tracked mono caps extract with stray spaces ("T HROUGH"), so parity is checked against the
    # page text with all whitespace and punctuation removed: every source word must appear.
    flat = re.sub(r"[^a-z0-9]", "", raw.lower()); need = b.norm(b.md_words(rendered_src))
    miss = {w: c for w, c in need.items() if w not in flat}
    print(f"parity: {sum(need.values())} source words, {sum(miss.values())} missing")
    if miss: ok = False; print("FAIL missing words:", dict(list(miss.items())[:20]))
    print("VERIFY", "PASS" if ok else "FAIL")
    return ok

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source"); ap.add_argument("out")
    ap.add_argument("--tokens"); ap.add_argument("--verify", action="store_true")
    ap.add_argument("--html", action="store_true")
    a = ap.parse_args()
    b.load_tokens(a.tokens); b.ensure_fonts()
    meta, body = b.parse_front_matter(open(a.source, encoding="utf8").read())
    for issue in b.lint(meta, body):
        print("lint:", issue, file=sys.stderr)
    doc, rendered = build(meta, body)
    if a.html: open(a.out + ".html", "w", encoding="utf8").write(doc)
    import logging; logging.getLogger("weasyprint").setLevel(logging.ERROR)
    from weasyprint import HTML
    try: HTML(string=doc).write_pdf(a.out, pdf_tags=True, custom_metadata=True)
    except TypeError: HTML(string=doc).write_pdf(a.out)
    print(f"wrote {a.out} {os.path.getsize(a.out) // 1024} KB")
    if a.verify: sys.exit(0 if verify(a.out, rendered) else 1)

if __name__ == "__main__":
    main()
