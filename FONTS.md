# Fonts

Two families are vendored in `generators/fonts/` so the renders build without a network fetch and
without depending on what happens to be installed locally.

| Family | Files | Licence |
| --- | --- | --- |
| Inter Tight | `InterTight.ttf` | SIL Open Font License 1.1 |
| JetBrains Mono | `JetBrainsMono-Regular.ttf`, `JetBrainsMono-SemiBold.ttf` | SIL Open Font License 1.1 |

Both licences permit redistribution, including bundling inside another work, provided the font
files are not sold on their own and the licence travels with them. Upstream:

- Inter Tight: https://github.com/rsms/inter
- JetBrains Mono: https://github.com/JetBrains/JetBrainsMono

Anyone redistributing this repository as a package should carry the OFL text alongside the font
files. It is not reproduced here because the fonts are vendored for the build rather than published
as a font release.

## How they are used

Inter Tight is the display and body face, weights 200 to 450, with negative tracking, and never bold
at display size. Instrument Serif italic is the accent face and is loaded from the web rather than
vendored, because nothing in this repository renders it. JetBrains Mono is chrome only: uppercase,
letter spacing +0.18em, used for file codes and section markers and never for body text.

`c9d-consulting-brand/references/visual-system.md` is the authority on all three.
