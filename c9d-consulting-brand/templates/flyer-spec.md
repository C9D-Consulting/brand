# Flyer Spec

> **STATUS: PROPOSED, NOT LOCKED.**
>
> This specification applies The Dossier system to a one-page flyer or service sheet. It was not part of the locked source artifacts. Treat it as a starting point for review with the Principal, not as locked system.

A flyer is one US Letter page, screen mode (dark ground, full bleed), built from markdown by `generators/c9d_flyer_build.py`. It shares tokens, fonts, front matter parsing and the inline dialect with `c9d_pdf_build.py`. Use it for service sheets, partner-program attachments and leave-behinds. Anything longer than one page is a document and goes through `c9d_pdf_build.py`.

```
python3 c9d_flyer_build.py source.md out.pdf --verify
```

## Front matter

The eight document keys (`file_id`, `classification`, `title`, `subtitle`, `prepared_for`, `prepared_by`, `version`, `section_marker`) plus:

| Key | Use |
| --- | --- |
| `eyebrow` | Mono line above the title, for example `AI Strategy & Enablement · Service Sheet` |
| `tagline` | Footer line; defaults to the primary tagline, "The playbook, not the deck." |

The title over 22 characters is split into two balanced lines. The subtitle is the lede and may carry one `*italic*` accent.

## Bands

`## EYEBROW · Title` opens a band. The layout follows from what the band contains:

| Layout | Content | Renders as |
| --- | --- | --- |
| brief | One table plus paragraphs | Key/value column (5) beside prose (7) under the Title as a heading. The table header row is a label and is not rendered. |
| strip | One table, no paragraphs | One numbered column per row; cells are name, window, work |
| split | Exactly two `###` subsections | First narrow, second wide; each `###` is that column's eyebrow |
| cards | `#### ID · Title` blocks with paragraphs | Side-by-side cards on `--bg-2` |

In split and cards bands the `##` line is a structural label and is not rendered.

## Inline

`**bold**` ink bright SemiBold, `*italic*` Instrument Serif, `` `mono` `` sodium amber mono, `[text](https://...)` amber links. Reserve mono for measured figures, since amber indexes the proof.

## Chrome

Mono metadata row at the top (file id, classification in stamp, `§ section_marker`, version). Footer: wordmark with C9D in stamp, the attribution from tokens.json, the tagline and `c9d.consulting`.

## Verify

`--verify` fails on: non-brand or unembedded fonts, more than one page, missing attribution, or any rendered source word missing from the PDF text. Then render with `pdftoppm -r 80 -png` and look.

## Rules

- No vendor logos. Vendor capability names only as the vendor's own documentation names them.
- No reference-client names, no em-dashes, no refused vocabulary, full name "C9D Consulting".
