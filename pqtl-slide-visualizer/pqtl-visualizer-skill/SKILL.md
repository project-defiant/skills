---
name: pqtl-slide-visualizer
description: >
  Use this skill to convert structured JSON output from the pQTL Olink publication
  reviewer into polished PowerPoint slide decks (and optionally PDF). Trigger whenever
  the user says "visualize the pQTL analysis", "make slides from the JSON", "generate
  slides from the review", "turn the pQTL JSON into a deck", or "create a presentation
  from the Olink reviewer output". Also trigger when the user uploads or pastes a JSON
  that matches the pQTL reviewer schema (contains keys like "paper", "study_design",
  "olink_platform", "gwas_methods", "post_gwas", etc.) and asks for a slide deck,
  report, or presentation.
---

# pQTL Slide Visualizer

Converts the structured JSON output from the **pQTL Olink Publication Reviewer** into
a polished, 6-slide PowerPoint deck with an optional PDF export.

## What this skill produces

A 6-slide PPTX (+ optional PDF) covering:

| Slide | Content |
|-------|---------|
| 1 | Title — paper title, authors, journal, year, DOI, key identity tags |
| 2 | Study Design & Population — stat cards, ancestry table, cohort names |
| 3 | Olink Platform & Proteomics QC — panel stats, QC parameters, bridging |
| 4 | Genotyping & GWAS Methodology — arrays, imputation, thresholds, covariates |
| 5 | Post-GWAS Analyses — fine-mapping, colocalization, epitope artifacts, trans hotspots |
| 6 | Mendelian Randomization & Data Availability — MR details + data access banner |

---

## Usage

### Step 1 — Obtain the JSON

The JSON must come from the **pQTL Olink Publication Reviewer** skill output, or match
its schema (see `references/schema.md`). The user may paste it directly, upload a `.json`
file, or it may already be in context from a prior extraction step.

### Step 2 — Save JSON to disk

If the JSON is pasted inline or in context:

```bash
cat > /home/claude/pqtl_review.json << 'EOF'
<paste JSON here>
EOF
```

If it was uploaded, check `/mnt/user-data/uploads/` for the file.

### Step 3 — Run the visualizer

```bash
python3 /mnt/skills/user/pqtl-slide-visualizer/scripts/pqtl_to_slides.py \
  /home/claude/pqtl_review.json \
  /home/claude/pqtl_output.pptx
```

Optional: add `--pdf` to also generate a PDF alongside the PPTX:

```bash
python3 /mnt/skills/user/pqtl-slide-visualizer/scripts/pqtl_to_slides.py \
  /home/claude/pqtl_review.json \
  /home/claude/pqtl_output.pptx \
  --pdf
```

### Step 4 — Visual QA (recommended)

Convert to images and inspect:

```bash
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf /home/claude/pqtl_output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 /home/claude/pqtl_output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Then `view` each image. Look for text overflow in cards (especially the Epitope Artifacts
card on slide 5 if the method string is long) and adjust as needed.

### Step 5 — Deliver

```bash
cp /home/claude/pqtl_output.pptx /mnt/user-data/outputs/
# If PDF was generated:
cp /home/claude/pqtl_output.pdf /mnt/user-data/outputs/
```

Then call `present_files` with the output path(s).

---

## Handling null / missing fields

The script degrades gracefully: any field that is `null` in the JSON renders as
"Not reported" in muted gray. No slide is skipped. Cards with all-null content
still appear (they show "Not reported" for every row), which correctly signals
data quality gaps to the reader.

---

## Dependencies

The script uses **PptxGenJS** (Node.js), which must be installed globally:

```bash
npm install -g pptxgenjs
```

Check availability with:

```bash
node -e "require('pptxgenjs')" && echo ok
```

PDF conversion uses LibreOffice via the shared `soffice.py` wrapper (already available
in the skill environment). PDF-to-image uses `pdftoppm` (Poppler).

---

## Customization notes

- **Color palette**: defined as the `C` object near the top of the generated JS.
  The current palette is "Ocean Executive" (deep navy titles, royal blue headers, cyan
  accents). To change colors, modify `C` constants in `scripts/pqtl_to_slides.py`.
- **Slide count**: the 6-slide structure maps 1:1 to the reviewer's 7 domains
  (domains 6 and 7 are combined on slide 6). Adding a new domain = add a new slide
  function in `build_js()`.
- **Font**: Calibri throughout. Change `fontFace` strings to switch.

---

## Schema reference

See `references/schema.md` for the full JSON field list and types.
