# Fonts

Two families are vendored in `generators/fonts/` so the renders build without a network fetch and
without depending on what happens to be installed locally.

| Family | Files | Licence |
| --- | --- | --- |
| Inter Tight | `InterTight.ttf` | SIL Open Font License 1.1 |
| JetBrains Mono | `JetBrainsMono-Regular.ttf`, `JetBrainsMono-SemiBold.ttf` | SIL Open Font License 1.1 |

Both licences permit redistribution, including bundling inside another work, provided the font
files are not sold on their own and the licence travels with them. Condition 2 of the OFL requires
that each copy carry the copyright notice and the licence, and publishing this repository is a
copy, so both licence texts sit beside the fonts they cover:

| Family | Upstream | Licence file |
| --- | --- | --- |
| Inter Tight | https://github.com/rsms/inter-tight | `generators/fonts/OFL-InterTight.txt` |
| JetBrains Mono | https://github.com/JetBrains/JetBrainsMono | `generators/fonts/OFL-JetBrainsMono.txt` |

Each file is the upstream text, unedited, and its copyright line matches the one the font binary
declares in its own name table. If a font is ever replaced or upgraded, replace its licence file
from the same release.

## How they are used

Inter Tight is the display and body face, weights 200 to 450, with negative tracking, and never bold
at display size. Instrument Serif italic is the accent face and is loaded from the web rather than
vendored, because only the Word and PDF generators embed it and they fetch it on first run.
JetBrains Mono is chrome only: uppercase, letter spacing +0.18em, used for file codes and section
markers and never for body text.

The Word and PDF generators need more. `generators/c9d_docx_build.py` embeds up to seven faces,
four static Inter Tight weights, two JetBrains Mono weights and Instrument Serif italic, because a
Word file that names a font it cannot supply is not a branded document. On first run it fetches the
upstream variable fonts from the Google Fonts repository, instances the static weights into
`generators/fonts/` beside the vendored files, and subsets each face into the document it builds.
Those instanced files are git-ignored, so the vendored set above stays the only fonts committed
here. `c9d_pdf_build.py` uses the same cache and file names. `c9d-operating-stack` has carried its
own copy of the Word generator; the file in `generators/` is the source of record.

`c9d-consulting-brand/references/visual-system.md` is the authority on all three.
