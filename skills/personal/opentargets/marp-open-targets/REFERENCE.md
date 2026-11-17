# Open Targets Marp theme — reference

Verified working implementation. Copy blocks verbatim rather than re-deriving them — this
has already been rendered and visually checked (see "Verified" below).

## Palette

Approximated by eye from an Open Targets reference deck's screenshots — not sourced from
an official brand guide. Good enough as the default; swap these six custom properties if
exact hex values ever surface (e.g. a brand guide or Figma file).

| Variable | Hex | Used for |
|---|---|---|
| `--ot-navy` | `#163A5F` | title-slide panel gradient end, presenter name |
| `--ot-blue` | `#2C77B5` | "Presented by" / role text, h2 color on content slides |
| `--ot-blue-mid` | `#4A93CB` | title-slide panel gradient start |
| `--ot-triangle` | `#6FA1CE` | corner-triangle fill (every slide) |
| `--ot-gray` | `#58595B` | "Open Targets" wordmark text |
| `--ot-text` | `#141414` | headings / body text |

## Front matter block

Paste into (or merge into) the deck's YAML front matter:

```yaml
marp: true
size: 16:9
footer: |
  <img src="assets/otar-logo.png" alt="" /><span>Open Targets</span>
style: |
  :root {
    --ot-navy: #163A5F;
    --ot-blue: #2C77B5;
    --ot-blue-mid: #4A93CB;
    --ot-triangle: #6FA1CE;
    --ot-gray: #58595B;
    --ot-text: #141414;
  }

  section {
    font-family: Arial, Helvetica, sans-serif;
    color: var(--ot-text);
    background: #ffffff;
    padding: 56px 64px;
    position: relative;
    overflow: hidden;
  }

  section h1 {
    font-size: 36px;
    font-weight: 700;
    color: var(--ot-text);
    margin: 0 0 0.3em;
  }

  section h2 {
    font-size: 22px;
    font-weight: 400;
    color: var(--ot-blue);
    margin: 0;
  }

  /* corner triangle — every slide */
  section::before {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 30%;
    height: 44%;
    background: var(--ot-triangle);
    clip-path: polygon(0 100%, 0 28%, 68% 100%);
    z-index: 0;
  }

  /* logo mark — bottom right, every slide except the title slide */
  section footer {
    position: absolute;
    right: 36px;
    bottom: 28px;
    left: auto;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--ot-gray);
    z-index: 1;
  }

  section footer img {
    height: 26px;
    width: auto;
    display: block;
  }

  section > * {
    position: relative;
    z-index: 2;
  }

  /* ---- Title slide ---- */
  section.title {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 70px 90px;
  }

  section.title footer {
    display: none;
  }

  section.title h1,
  section.title h2 {
    max-width: 54%;
  }

  section.title h1 {
    font-size: 40px;
    line-height: 1.25;
    margin-bottom: 10px;
  }

  section.title h2 {
    font-style: italic;
    font-weight: 400;
    color: var(--ot-text);
  }

  .ot-diagonal {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 42%;
    background: linear-gradient(160deg, var(--ot-blue-mid) 0%, var(--ot-navy) 75%);
    z-index: 0;
  }

  .ot-logo-title {
    position: absolute;
    left: 70px;
    top: 48px;
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 2;
  }

  .ot-logo-title img {
    height: 40px;
    width: auto;
    display: block;
  }

  .ot-logo-title span {
    font-size: 18px;
    color: var(--ot-gray);
  }

  .ot-presenter {
    margin-top: 56px;
  }

  .ot-presenter p {
    margin: 0 0 4px;
  }

  .ot-presenter .presented-by {
    color: var(--ot-blue);
    font-size: 14px;
  }

  .ot-presenter .presenter-name {
    color: var(--ot-navy);
    font-weight: 700;
    font-size: 16px;
  }

  .ot-presenter .presenter-role {
    color: var(--ot-blue);
    font-size: 13px;
  }
```

Note: `section > * { position: relative; z-index: 2; }` is what keeps every slide's real
content painting above the corner triangle (z-index 0) and footer (z-index 1) — don't drop
it when merging into a deck that already has its own `style:` rules.

## Title slide markup

The first slide only. Fill the four placeholders from context (deck title, subtitle,
presenter name, presenter role/affiliation):

```markdown
<!-- _class: title -->

<div class="ot-diagonal"></div>
<div class="ot-logo-title">
  <img src="assets/otar-logo.png" alt="" />
  <span>Open Targets</span>
</div>

# {{DECK_TITLE}}

## {{DECK_SUBTITLE}}

<div class="ot-presenter">
<p class="presented-by">Presented by</p>
<p class="presenter-name">{{PRESENTER_NAME}}</p>
<p class="presenter-role">{{PRESENTER_ROLE}}</p>
</div>
```

Every slide *after* this one needs no extra markup at all — the corner triangle and the
footer logo lockup apply automatically via the global CSS above.

## Scaffolding a brand-new deck

1. `mkdir -p assets && cp <this-skill>/assets/otar-logo.png ./assets/otar-logo.png` (path
   relative to wherever the deck's markdown file will live).
2. Write the markdown file: front-matter block above, then the title-slide markup, then
   `---` and the deck's actual content slides.
3. Render to check: `npx @marp-team/marp-cli@latest presentation.md -o preview.html --allow-local-files`.

## Retrofitting an existing deck

1. Read the deck's current front matter. Add `size: 16:9` if no size is set. Add the
   `footer:` key. Merge the `style:` CSS block in — if the deck already defines its own
   `style:` rules, combine them (don't delete the existing rules, and don't create two
   `style:` keys).
2. Find the deck's first slide. Add `<!-- _class: title -->` as its first line. Insert the
   `.ot-diagonal` and `.ot-logo-title` divs and the `.ot-presenter` block. Reuse the
   existing `#`/`##` title and subtitle text as-is rather than inventing new copy.
3. Copy `assets/otar-logo.png` into the target repo if it isn't already present there.
4. Do not touch any other slide's markdown — they inherit the triangle + footer
   automatically once the front matter above is in place.
5. Render to check, same command as above (`--allow-local-files` required).

## Gotchas

- **Never put the logo/wordmark text on `section::after`.** Marp's base theme uses
  `section::after { content: attr(data-marpit-pagination); ... }` for page numbers, and
  when a custom theme also declares `content` on `section::after`, Marp's own CSS
  processing silently drops the custom `content` value (confirmed by inspecting the
  rendered HTML's compiled `<style>` block — every other declared property survived,
  only `content` was stripped). Marp's `footer:` front-matter directive inserts a real
  `<footer>` DOM element instead, which has no such conflict — that's why the theme uses
  `section footer { ... }` rather than `section::after { content: "Open Targets"; ... }`.
- Rendering (HTML/PDF/PNG export, and the VS Code Marp preview) needs
  `--allow-local-files` once a deck references a local image like the logo.
- The `assets/otar-logo.png` bundled here is the icon mark only (no wordmark baked in,
  transparent background, roughly square) — always pair it with a literal "Open Targets"
  text span, never rely on the image alone to carry the wordmark.
- Keep this theme chrome-only. A specific talk's content rules (evidence-required tags,
  claims-to-avoid lists, act/slide numbering, etc.) belong in that repo's own CLAUDE.md,
  not in this skill.
- v1 intentionally has no additional slide-type templates (stat callouts, comparison
  tables, section dividers) beyond the title slide and the shared per-slide chrome. Add
  them here only once the same shape has recurred across 2+ real decks.

## Verified

Rendered via `@marp-team/marp-cli` and visually inspected (title slide: logo + title +
subtitle + presenter block over a flat right-side color panel, corner triangle bottom-left;
second/content slide: same corner triangle + footer logo lockup, no title-slide-only
elements) in the `multi-ancestry-fm` repo, 2026-08-25.
