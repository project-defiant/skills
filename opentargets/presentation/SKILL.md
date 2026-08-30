---
name: marp-open-targets
description: Applies the Open Targets brand theme to a Marp (markdown-to-slides) presentation — a navy/blue palette, a corner-triangle motif and footer logo lockup on every slide, and a bespoke title slide with a right-side color panel and top-left logo. Use when creating a new Open Targets presentation, when asked to make a Marp deck "Open Targets branded" or match the "OT theme", or when retrofitting Open Targets styling onto an existing Marp markdown deck. Do not use for a generic Marp deck with no Open Targets branding request.
---

# Marp: Open Targets theme

Packages the reusable Open Targets visual theme for [Marp](https://marp.app/) decks: the brand color palette, per-slide chrome (corner triangle + footer logo), and a title-slide layout. Visual/chrome only — it does not impose any particular talk's content structure, slide numbering, or evidence-tracking discipline; those stay in the target repo's own docs.

## Quick start

1. Copy `assets/otar-logo.png` from this skill into the target repo (e.g. `assets/otar-logo.png` sitting next to the deck's markdown file).
2. Paste the front-matter block and title-slide markup from [REFERENCE.md](REFERENCE.md) into the deck, filling in `{{DECK_TITLE}}`, `{{DECK_SUBTITLE}}`, `{{PRESENTER_NAME}}`, `{{PRESENTER_ROLE}}` from conversation context.
3. Every other slide inherits the corner triangle + footer automatically — no further per-slide markup needed.
4. Render with `npx @marp-team/marp-cli@latest <file>.md -o preview.html --allow-local-files` — the `--allow-local-files` flag is required because the theme loads a local logo image.

## Workflows

### New deck
Create the markdown file with the front matter + title slide from REFERENCE.md up front, then add content slides normally — they pick up the theme for free via the global CSS.

### Retrofit an existing deck
1. Merge the `footer:` and `style:` blocks from REFERENCE.md into the deck's existing YAML front matter (merge with, don't clobber, any style rules already there).
2. Promote the deck's first slide to the title-slide treatment: add `<!-- _class: title -->`, the `.ot-diagonal` and `.ot-logo-title` divs, and the `.ot-presenter` block, keeping the existing title/subtitle text.
3. Copy the logo asset into the repo if it isn't already there.
4. Leave every other slide's content untouched — the chrome applies globally via the CSS, nothing per-slide to add.

## Key gotcha

Marp's base theme reserves `content` on `section::after` for page-number pagination and silently drops a custom `content` value set there. Use Marp's `footer:` front-matter directive (a real `<footer>` element) for the logo+wordmark instead — never a `::after` pseudo-element for text content.

See [REFERENCE.md](REFERENCE.md) for the full CSS, the title-slide template, and the complete retrofit checklist.
