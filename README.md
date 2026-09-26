# C9D Consulting brand

The Dossier, v2.3. The source of record for the C9D Consulting brand system.

A practice of Brandon Wilburn.

## Why this repository exists

The brand had been living in four places at once: a Google Drive folder, a second Google Drive
folder, two zip archives both claiming v2.3, and an installed Claude skill. Nothing declared which
was current, and the two zips were forty kilobytes apart.

This repository is the answer. Everything the brand is, and everything generated from it, is here.
Every other copy is distribution.

## Where a brand file belongs

| Home | Holds | Test |
| --- | --- | --- |
| This repository | Tokens, logo sources, references, specs, generators, and every render they produce | It is generated, or it generates something |
| The site deploy | `c9d-banner-og-1200x630.png`, the favicons, anything fetched by URL | A machine requests it over HTTP |
| Google Drive, Practice, `01 Brand` | The brand guide, the deck and document templates, and a pointer here | A person opens it by hand and cannot regenerate it |

A render is never edited. It is regenerated. That is what makes a build artifact safe to commit and
unsafe to keep loose in a folder where someone can open it, change it, and leave two versions of the
truth behind.

## Layout

```
c9d-consulting-brand/     The brand skill. Strategic foundation and production assets.
  SKILL.md                Entry point, 21 strategic invariants
  references/             Foundation, visual system, voice library, site copy, engagement architecture
  assets/tokens.json      Design tokens, machine readable
  assets/tokens.css       The same tokens as custom properties
  assets/logos/           Logo sources (SVG) and their renders (PNG)
  templates/              Word and PowerPoint templates, architecture diagrams, format specs

c9d-brand-guard/          The compliance skill. Verifies artifacts against v2.3.

generators/               Scripts that produce the renders below
  fonts/                  Inter Tight and JetBrains Mono, see FONTS.md

renders/                  Build output. Regenerable. Do not hand edit.
  notion-icons/           Database and page icons for the Notion workspace
  notion-covers/          Teamspace and template covers
  drive-themes/           Shared drive banners, 1280x144

docs/PACKAGE.md           The distribution archive's own README
VERSION                   2.3
```

Both skills carry the same version tag. When the strategic foundation moves, both rebuild together.
Do not mix versions.

## Build

Requires Python 3 with Pillow.

```
make            Regenerate every render
make icons      Notion database and page icons
make covers     Notion teamspace and template covers
make themes     Google shared drive banners
make dist       Build the installable skills archive into dist/
make clean      Remove dist/
```

The generators read the fonts in `generators/fonts/` and the palette compiled into each script. When
a token changes, change it in `assets/tokens.json` first, then in the generators, then rebuild. The
duplication between the two is a known gap and the next thing worth fixing.

## Installing the skills

Copy both skill folders into your Claude user skills directory, or drop them into a project's
working directory to scope them to that project.

```
c9d-consulting-brand/
c9d-brand-guard/
```

`docs/PACKAGE.md` describes what each skill does and when each one loads.

## Releasing

A release is a version bump, a rebuild of every render, and one archive. Tag the commit with the
version. The archive in `dist/` is the only artifact that should ever be handed to anyone as a file,
and it carries its version in its name, so a stale copy is obvious as a stale copy.

## What is deliberately not here

Executed agreements, client material and anything else the practice files in Google Drive. This
repository holds the brand and nothing else.
