#!/usr/bin/env python3
"""
pQTL Olink Publication Reviewer — Slide Visualizer
Converts structured JSON output from the pQTL reviewer into a polished PDF slide deck.

Usage:
    python pqtl_to_slides.py <input.json> [output.pptx]
    python pqtl_to_slides.py <input.json> --pdf  # also convert to PDF
"""

import json
import os
import sys
import subprocess
import tempfile
import argparse

def load_json(path):
    with open(path) as f:
        return json.load(f)

def safe(val, fallback="Not reported"):
    if val is None:
        return fallback
    if isinstance(val, bool):
        return "Yes" if val else "No"
    if isinstance(val, list):
        if not val:
            return fallback
        return ", ".join(str(v) for v in val)
    return str(val)

def build_js(data, output_path):
    """Generate the PptxGenJS script as a string."""

    paper = data.get("paper", {})
    study = data.get("study_design", {})
    olink = data.get("olink_platform", {})
    geno = data.get("genotyping", {})
    gwas = data.get("gwas_methods", {})
    post = data.get("post_gwas", {})
    mr = data.get("mendelian_randomization", {})
    da = data.get("data_availability", {})

    title = paper.get("title", "pQTL Study Review")
    authors = paper.get("authors", "")
    journal = paper.get("journal", "")
    year = paper.get("year", "")
    doi = paper.get("doi", "")

    # Ancestry table rows
    ancestries = study.get("ancestries", [])
    ancestry_rows = []
    for a in ancestries:
        ancestry_rows.append({"group": a.get("group",""), "n": a.get("n","")})

    # Trans hotspots
    hotspots = post.get("trans_hotspots", []) or []
    hotspot_str = "; ".join(
        f"{h['locus']} ({h.get('n_proteins_influenced','?')} proteins)"
        for h in hotspots
    ) if hotspots else "Not reported"

    # Fine mapping
    fm = post.get("fine_mapping", {}) or {}
    coloc = post.get("colocalization", {}) or {}
    epi = post.get("epitope_artifact_assessment", {}) or {}

    covariates = gwas.get("covariates", []) or []
    cov_str = ", ".join(covariates) if covariates else "Not reported"

    mr_proteins = mr.get("proteins_tested", []) or []
    mr_outcomes = mr.get("outcomes_tested", []) or []
    mr_methods = mr.get("methods_used", []) or []

    def jstr(v):
        """Escape for JS string literal."""
        if v is None:
            return "Not reported"
        return str(v).replace("\\","\\\\").replace('"','\\"').replace('\n',' ')

    js = f"""
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "{jstr(title)}";

// ── Color palette (Ocean Executive) ──────────────────────────────────────────
const C = {{
  bg:       "0A1628",   // deep navy (dark slide bg)
  bgLight:  "F7F9FC",   // near white (light slide bg)
  primary:  "1565C0",   // royal blue
  accent:   "00BCD4",   // cyan accent
  accent2:  "26A69A",   // teal
  accent3:  "EF5350",   // red for alerts
  text:     "1A1A2E",   // near-black
  textMid:  "455A64",   // medium gray
  textLight:"ECEFF1",   // light (on dark)
  card:     "FFFFFF",   // white cards
  cardAlt:  "E3F2FD",   // light blue cards
  border:   "90CAF9",   // card border
  null:     "B0BEC5",   // greyed-out null values
  green:    "2E7D32",
  amber:    "F57F17",
}};

const makeShadow = () => ({{ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 }});

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 1: Title
// ─────────────────────────────────────────────────────────────────────────────
let s1 = pres.addSlide();
s1.background = {{ color: C.bg }};

// Accent stripe
s1.addShape(pres.shapes.RECTANGLE, {{
  x: 0, y: 2.6, w: 10, h: 0.06, fill: {{ color: C.accent }}, line: {{ color: C.accent }}
}});

// Large title
s1.addText("{jstr(title)}", {{
  x: 0.6, y: 0.5, w: 8.8, h: 2.0,
  fontSize: 28, bold: true, color: C.textLight, fontFace: "Calibri",
  align: "left", valign: "bottom", wrap: true
}});

// Meta info
s1.addText("{jstr(authors)}", {{
  x: 0.6, y: 2.75, w: 8.8, h: 0.45,
  fontSize: 12, color: C.border, fontFace: "Calibri", align: "left", italic: true
}});

s1.addText("{jstr(journal)}  |  {jstr(str(year))}  |  DOI: {jstr(doi)}", {{
  x: 0.6, y: 3.25, w: 8.8, h: 0.4,
  fontSize: 11, color: C.null, fontFace: "Calibri", align: "left"
}});

// Tag pills (study identity summary)
const tags = [
  "Cohort: {jstr(safe(study.get('cohort_names')))}",
  "N = {jstr(safe(study.get('total_n')))}",
  "{jstr(safe(olink.get('panel_name')))}",
  "{jstr(safe(study.get('design_type')))}",
];
let tagX = 0.6;
tags.forEach(t => {{
  const w = Math.max(1.5, t.length * 0.115 + 0.3);
  s1.addShape(pres.shapes.ROUNDED_RECTANGLE, {{
    x: tagX, y: 3.85, w: w, h: 0.38,
    fill: {{ color: C.primary }}, line: {{ color: C.accent }}, rectRadius: 0.06
  }});
  s1.addText(t, {{
    x: tagX, y: 3.85, w: w, h: 0.38,
    fontSize: 10, color: "FFFFFF", fontFace: "Calibri", align: "center", valign: "middle"
  }});
  tagX += w + 0.15;
}});

s1.addText("pQTL Olink Publication Review", {{
  x: 0.6, y: 5.1, w: 8.8, h: 0.35,
  fontSize: 10, color: C.null, fontFace: "Calibri", align: "left"
}});

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 2: Study Design & Ancestry
// ─────────────────────────────────────────────────────────────────────────────
let s2 = pres.addSlide();
s2.background = {{ color: C.bgLight }};

s2.addText("Study Design & Population", {{
  x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 22, bold: true,
  color: C.primary, fontFace: "Calibri", align: "left"
}});
s2.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.75, w: 9, h: 0.04, fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});

// Key stats row
const stats = [
  {{ label: "Sample Size", value: "{jstr(safe(study.get('total_n')))}", color: C.primary }},
  {{ label: "Design", value: "{jstr(safe(study.get('design_type')))}", color: C.accent2 }},
  {{ label: "Matrix", value: "{jstr(safe(study.get('sample_matrix')))}", color: C.accent }},
  {{ label: "Multi-ancestry", value: "{jstr(safe(study.get('multi_ancestry_analysis')))}", color: C.primary }},
];
stats.forEach((st, i) => {{
  const x = 0.5 + i * 2.35;
  s2.addShape(pres.shapes.RECTANGLE, {{
    x, y: 0.9, w: 2.2, h: 1.1,
    fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }},
    shadow: makeShadow()
  }});
  s2.addShape(pres.shapes.RECTANGLE, {{
    x, y: 0.9, w: 2.2, h: 0.08,
    fill: {{ color: st.color }}, line: {{ color: st.color }}
  }});
  s2.addText(st.value, {{
    x, y: 0.98, w: 2.2, h: 0.6,
    fontSize: 16, bold: true, color: C.text, fontFace: "Calibri",
    align: "center", valign: "middle", wrap: true
  }});
  s2.addText(st.label, {{
    x, y: 1.58, w: 2.2, h: 0.32,
    fontSize: 9, color: C.textMid, fontFace: "Calibri", align: "center"
  }});
}});

// Ancestry table
const ancestryData = {json.dumps(ancestry_rows)};
const cohorts = {json.dumps(study.get('cohort_names', []) or [])};

s2.addText("Ancestry Breakdown", {{
  x: 0.5, y: 2.15, w: 4.5, h: 0.35,
  fontSize: 13, bold: true, color: C.text, fontFace: "Calibri"
}});

if (ancestryData.length > 0) {{
  const tableRows = [
    [
      {{ text: "Ancestry Group", options: {{ bold: true, color: "FFFFFF", fill: {{ color: C.primary }}, align: "center" }} }},
      {{ text: "N", options: {{ bold: true, color: "FFFFFF", fill: {{ color: C.primary }}, align: "center" }} }}
    ],
    ...ancestryData.map((a, i) => [
      {{ text: a.group, options: {{ fill: {{ color: i%2===0 ? C.card : C.cardAlt }}, align: "left" }} }},
      {{ text: String(a.n || "—"), options: {{ fill: {{ color: i%2===0 ? C.card : C.cardAlt }}, align: "center" }} }}
    ])
  ];
  s2.addTable(tableRows, {{
    x: 0.5, y: 2.55, w: 4.2, colW: [3.0, 1.2],
    border: {{ pt: 1, color: C.border }},
    fontSize: 12, fontFace: "Calibri", h: 0.35
  }});
}} else {{
  s2.addText("Ancestry breakdown not reported", {{
    x: 0.5, y: 2.55, w: 4.2, h: 0.5,
    fontSize: 11, color: C.null, italic: true, fontFace: "Calibri"
  }});
}}

// Cohort names
s2.addText("Cohort(s)", {{
  x: 5.1, y: 2.15, w: 4.5, h: 0.35,
  fontSize: 13, bold: true, color: C.text, fontFace: "Calibri"
}});
cohorts.forEach((c, i) => {{
  s2.addShape(pres.shapes.RECTANGLE, {{
    x: 5.1, y: 2.55 + i*0.45, w: 4.3, h: 0.38,
    fill: {{ color: i%2===0 ? C.cardAlt : C.card }}, line: {{ color: C.border, pt: 1 }}
  }});
  s2.addText(c, {{
    x: 5.2, y: 2.55 + i*0.45, w: 4.1, h: 0.38,
    fontSize: 12, color: C.text, fontFace: "Calibri", valign: "middle"
  }});
}});

// Ancestry-specific pQTLs note
s2.addText(
  "Ancestry-specific pQTLs: {jstr(safe(study.get('ancestry_specific_pqtls_reported')))}  |  Count: {jstr(safe(study.get('n_ancestry_specific_pqtls')))}",
  {{
    x: 0.5, y: 5.05, w: 9, h: 0.35,
    fontSize: 10, color: C.textMid, fontFace: "Calibri", italic: true
  }}
);

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 3: Olink Platform & Proteomics QC
// ─────────────────────────────────────────────────────────────────────────────
let s3 = pres.addSlide();
s3.background = {{ color: C.bgLight }};

s3.addText("Olink Platform & Proteomics QC", {{
  x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 22, bold: true,
  color: C.primary, fontFace: "Calibri"
}});
s3.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.75, w: 9, h: 0.04, fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});

// Top stat cards: proteins assayed and with pQTL
const protStats = [
  {{ label: "Panel", val: "{jstr(safe(olink.get('panel_name')))} {jstr(safe(olink.get('panel_version')))}" }},
  {{ label: "Proteins Assayed", val: "{jstr(safe(olink.get('n_proteins_assayed')))}" }},
  {{ label: "Proteins with ≥1 pQTL", val: "{jstr(safe(olink.get('n_proteins_with_pqtl')))}" }},
];
protStats.forEach((ps, i) => {{
  const x = 0.5 + i * 3.1;
  s3.addShape(pres.shapes.RECTANGLE, {{
    x, y: 0.88, w: 2.95, h: 1.0,
    fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}, shadow: makeShadow()
  }});
  s3.addText(ps.val, {{
    x, y: 0.9, w: 2.95, h: 0.6,
    fontSize: 18, bold: true, color: C.primary, fontFace: "Calibri",
    align: "center", valign: "middle", wrap: true
  }});
  s3.addText(ps.label, {{
    x, y: 1.5, w: 2.95, h: 0.3,
    fontSize: 9, color: C.textMid, fontFace: "Calibri", align: "center"
  }});
}});

// QC details as two columns
const qcLeft = [
  ["Batch/Plate Correction", "{jstr(safe(olink.get('npx_batch_correction_method')))}"],
  ["Intensity Normalization", "{jstr(safe(olink.get('npx_intensity_normalization')))}"],
  ["LOD Handling", "{jstr(safe(olink.get('lod_handling')))}"],
  ["LOD Exclusion Threshold", "{jstr(safe(olink.get('lod_exclusion_threshold_pct')))}"],
];
const qcRight = [
  ["Bridging Performed", "{jstr(safe(olink.get('bridging_performed')))}"],
  ["Bridge Samples (N)", "{jstr(safe(olink.get('n_bridge_samples')))}"],
  ["Bridging Reference", "{jstr(safe(olink.get('bridging_reference_dataset')))}"],
];

function drawKVPairs(slide, pairs, x, y, w) {{
  pairs.forEach(([k, v], i) => {{
    const bg = i % 2 === 0 ? C.card : C.cardAlt;
    slide.addShape(pres.shapes.RECTANGLE, {{
      x, y: y + i * 0.52, w, h: 0.48,
      fill: {{ color: bg }}, line: {{ color: C.border, pt: 1 }}
    }});
    slide.addText(k, {{
      x: x + 0.08, y: y + i*0.52, w: w*0.45, h: 0.48,
      fontSize: 10, bold: true, color: C.textMid, fontFace: "Calibri", valign: "middle"
    }});
    slide.addText(v, {{
      x: x + w*0.45, y: y + i*0.52, w: w*0.55, h: 0.48,
      fontSize: 10, color: C.text, fontFace: "Calibri", valign: "middle", wrap: true
    }});
  }});
}}

drawKVPairs(s3, qcLeft, 0.5, 2.0, 4.4);
drawKVPairs(s3, qcRight, 5.1, 2.0, 4.4);

s3.addText("NPX QC Parameters", {{
  x: 0.5, y: 1.95, w: 4.4, h: 0.3, fontSize: 11, bold: true,
  color: C.text, fontFace: "Calibri"
}});
s3.addText("Bridging & Multi-batch", {{
  x: 5.1, y: 1.95, w: 4.4, h: 0.3, fontSize: 11, bold: true,
  color: C.text, fontFace: "Calibri"
}});

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 4: Genotyping & GWAS Methods
// ─────────────────────────────────────────────────────────────────────────────
let s4 = pres.addSlide();
s4.background = {{ color: C.bgLight }};

s4.addText("Genotyping & GWAS Methodology", {{
  x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 22, bold: true,
  color: C.primary, fontFace: "Calibri"
}});
s4.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.75, w: 9, h: 0.04, fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});

const genoItems = [
  ["Genotyping Array", "{jstr(safe(geno.get('array')))}"],
  ["Imputation Reference", "{jstr(safe(geno.get('imputation_reference_panel')))}"],
  ["Imputation R²", "{jstr(safe(geno.get('imputation_r2_threshold')))}"],
  ["MAF Threshold", "{jstr(safe(geno.get('maf_threshold')))}"],
];
drawKVPairs(s4, genoItems, 0.5, 0.9, 4.4);
s4.addText("Genotyping", {{
  x: 0.5, y: 0.85, w: 4.4, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});

const mafNote = "{jstr(safe(geno.get('maf_appropriateness_note')))}";
s4.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 3.0, w: 4.4, h: 0.8,
  fill: {{ color: C.cardAlt }}, line: {{ color: C.accent, pt: 1 }}
}});
s4.addText("⚠ MAF Note: " + mafNote, {{
  x: 0.6, y: 3.0, w: 4.2, h: 0.8,
  fontSize: 9, italic: true, color: C.textMid, fontFace: "Calibri", valign: "middle", wrap: true
}});

const gwasItems = [
  ["Statistical Model", "{jstr(safe(gwas.get('statistical_model')))}"],
  ["Genome-wide Threshold", "{jstr(safe(gwas.get('significance_threshold_genomewide')))}"],
  ["Protein Bonferroni Correction", "{jstr(safe(gwas.get('bonferroni_correction_for_proteins')))}"],
  ["cis Threshold", "{jstr(safe(gwas.get('cis_threshold')))}"],
  ["trans Threshold", "{jstr(safe(gwas.get('trans_threshold')))}"],
  ["cis Window", "{jstr(safe(gwas.get('cis_window_size_kb')))} kb ({jstr(safe(gwas.get('cis_window_anchor')))})"],
];
drawKVPairs(s4, gwasItems, 5.1, 0.9, 4.4);
s4.addText("GWAS Methods", {{
  x: 5.1, y: 0.85, w: 4.4, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});

// Covariates
s4.addText("Covariates", {{
  x: 0.5, y: 3.95, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});
s4.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 4.3, w: 9, h: 0.9,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}
}});
s4.addText("{jstr(cov_str)}", {{
  x: 0.6, y: 4.3, w: 8.8, h: 0.9,
  fontSize: 10, color: C.text, fontFace: "Calibri", valign: "middle", wrap: true
}});

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 5: Post-GWAS Analyses
// ─────────────────────────────────────────────────────────────────────────────
let s5 = pres.addSlide();
s5.background = {{ color: C.bgLight }};

s5.addText("Post-GWAS Analyses", {{
  x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 22, bold: true,
  color: C.primary, fontFace: "Calibri"
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.75, w: 9, h: 0.04, fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});

// Fine-mapping card
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.88, w: 2.85, h: 2.0,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}, shadow: makeShadow()
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.88, w: 2.85, h: 0.35,
  fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});
s5.addText("Fine-Mapping", {{
  x: 0.5, y: 0.88, w: 2.85, h: 0.35,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: "Calibri",
  align: "center", valign: "middle"
}});
const fmPairs = [
  ["Performed", "{jstr(safe(fm.get('performed')))}"],
  ["Method", "{jstr(safe(fm.get('method')))}"],
  ["Credible Sets", "{jstr(safe(fm.get('n_credible_sets')))}"],
  ["PIP Threshold", "{jstr(safe(fm.get('pip_threshold')))}"],
];
fmPairs.forEach(([k, v], i) => {{
  s5.addText(k + ":", {{
    x: 0.55, y: 1.28 + i*0.37, w: 1.3, h: 0.35,
    fontSize: 9, bold: true, color: C.textMid, fontFace: "Calibri"
  }});
  s5.addText(v, {{
    x: 1.85, y: 1.28 + i*0.37, w: 1.4, h: 0.35,
    fontSize: 9, color: C.text, fontFace: "Calibri", wrap: true
  }});
}});

// Colocalization card
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 3.57, y: 0.88, w: 2.85, h: 2.0,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}, shadow: makeShadow()
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 3.57, y: 0.88, w: 2.85, h: 0.35,
  fill: {{ color: C.accent2 }}, line: {{ color: C.accent2 }}
}});
s5.addText("Colocalization", {{
  x: 3.57, y: 0.88, w: 2.85, h: 0.35,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: "Calibri",
  align: "center", valign: "middle"
}});
const colocPairs = [
  ["Performed", "{jstr(safe(coloc.get('performed')))}"],
  ["Method", "{jstr(safe(coloc.get('method')))}"],
  ["PP4 Threshold", "{jstr(safe(coloc.get('pp4_threshold')))}"],
  ["Traits Tested", "{jstr(safe(coloc.get('traits_tested')))}"],
];
colocPairs.forEach(([k, v], i) => {{
  s5.addText(k + ":", {{
    x: 3.62, y: 1.28 + i*0.37, w: 1.3, h: 0.35,
    fontSize: 9, bold: true, color: C.textMid, fontFace: "Calibri"
  }});
  s5.addText(v, {{
    x: 4.92, y: 1.28 + i*0.37, w: 1.4, h: 0.35,
    fontSize: 9, color: C.text, fontFace: "Calibri", wrap: true
  }});
}});

// Epitope artifact card
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 6.64, y: 0.88, w: 2.85, h: 2.0,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}, shadow: makeShadow()
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 6.64, y: 0.88, w: 2.85, h: 0.35,
  fill: {{ color: C.accent3 }}, line: {{ color: C.accent3 }}
}});
s5.addText("Epitope Artifacts", {{
  x: 6.64, y: 0.88, w: 2.85, h: 0.35,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: "Calibri",
  align: "center", valign: "middle"
}});
// Assessed row
s5.addText("Assessed:", {{
  x: 6.7, y: 1.28, w: 1.3, h: 0.35,
  fontSize: 9, bold: true, color: C.textMid, fontFace: "Calibri"
}});
s5.addText("{jstr(safe(epi.get('performed')))}", {{
  x: 8.0, y: 1.28, w: 1.4, h: 0.35,
  fontSize: 9, color: C.text, fontFace: "Calibri"
}});
// Method row (taller for wrapping)
s5.addText("Method:", {{
  x: 6.7, y: 1.65, w: 1.3, h: 0.7,
  fontSize: 9, bold: true, color: C.textMid, fontFace: "Calibri"
}});
s5.addText("{jstr(safe(epi.get('method')))}", {{
  x: 8.0, y: 1.65, w: 1.4, h: 0.7,
  fontSize: 9, color: C.text, fontFace: "Calibri", wrap: true
}});
// pQTLs flagged
s5.addText("Flagged:", {{
  x: 6.7, y: 2.4, w: 1.3, h: 0.35,
  fontSize: 9, bold: true, color: C.textMid, fontFace: "Calibri"
}});
s5.addText("{jstr(safe(epi.get('n_pqtls_flagged')))}", {{
  x: 8.0, y: 2.4, w: 1.4, h: 0.35,
  fontSize: 9, color: C.text, fontFace: "Calibri"
}});

// Colocalization key findings
s5.addText("Colocalization Key Findings", {{
  x: 0.5, y: 3.0, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 3.35, w: 9, h: 0.75,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}
}});
s5.addText("{jstr(safe(coloc.get('key_findings')))}", {{
  x: 0.6, y: 3.35, w: 8.8, h: 0.75,
  fontSize: 10, color: C.text, fontFace: "Calibri", valign: "middle", wrap: true
}});

// Trans hotspots
s5.addText("Trans-pQTL Hotspots", {{
  x: 0.5, y: 4.2, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});
s5.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 4.55, w: 9, h: 0.7,
  fill: {{ color: C.cardAlt }}, line: {{ color: C.border, pt: 1 }}
}});
s5.addText("{jstr(hotspot_str)}", {{
  x: 0.6, y: 4.55, w: 8.8, h: 0.7,
  fontSize: 10, color: C.text, fontFace: "Calibri", valign: "middle", wrap: true
}});

// ─────────────────────────────────────────────────────────────────────────────
// SLIDE 6: Mendelian Randomization & Data Availability
// ─────────────────────────────────────────────────────────────────────────────
let s6 = pres.addSlide();
s6.background = {{ color: C.bgLight }};

s6.addText("Mendelian Randomization & Data Access", {{
  x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 22, bold: true,
  color: C.primary, fontFace: "Calibri"
}});
s6.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.75, w: 9, h: 0.04, fill: {{ color: C.primary }}, line: {{ color: C.primary }}
}});

// MR section
const mrPerformed = "{jstr(safe(mr.get('performed')))}";
const mrColor = mrPerformed === "Yes" ? C.green : C.null;

s6.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 0.88, w: 9, h: 0.42,
  fill: {{ color: mrPerformed === "Yes" ? C.cardAlt : C.card }},
  line: {{ color: mrPerformed === "Yes" ? C.accent2 : C.border, pt: 1 }}
}});
s6.addText("MR Performed: " + mrPerformed, {{
  x: 0.6, y: 0.88, w: 8.8, h: 0.42,
  fontSize: 13, bold: true, color: mrColor, fontFace: "Calibri", valign: "middle"
}});

const mrPairs = [
  ["Proteins (exposures)", "{jstr(', '.join(mr_proteins) if mr_proteins else 'Not reported')}"],
  ["Outcomes tested", "{jstr(', '.join(mr_outcomes) if mr_outcomes else 'Not reported')}"],
  ["Methods used", "{jstr(', '.join(mr_methods) if mr_methods else 'Not reported')}"],
  ["F-statistics reported", "{jstr(safe(mr.get('f_statistics_reported')))}"],
];
drawKVPairs(s6, mrPairs, 0.5, 1.38, 9);

s6.addText("Key MR Findings", {{
  x: 0.5, y: 3.5, w: 9, h: 0.3, fontSize: 11, bold: true, color: C.text, fontFace: "Calibri"
}});
s6.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 3.85, w: 9, h: 0.75,
  fill: {{ color: C.card }}, line: {{ color: C.border, pt: 1 }}
}});
s6.addText("{jstr(safe(mr.get('key_findings')))}", {{
  x: 0.6, y: 3.85, w: 8.8, h: 0.75,
  fontSize: 10, color: C.text, fontFace: "Calibri", valign: "middle", wrap: true
}});

// Data availability
const dataPublic = {json.dumps(da.get('summary_stats_public'))};
const daColor = dataPublic === true ? C.green : dataPublic === false ? C.accent3 : C.null;
const daLabel = dataPublic === true ? "✓  Summary statistics PUBLICLY AVAILABLE" :
                dataPublic === false ? "✗  Summary statistics NOT publicly available" :
                "?  Data availability not reported";

s6.addShape(pres.shapes.RECTANGLE, {{
  x: 0.5, y: 4.75, w: 9, h: 0.55,
  fill: {{ color: dataPublic === true ? "E8F5E9" : dataPublic === false ? "FFEBEE" : C.card }},
  line: {{ color: daColor, pt: 2 }}
}});
s6.addText(daLabel, {{
  x: 0.6, y: 4.75, w: 6, h: 0.55,
  fontSize: 13, bold: true, color: daColor, fontFace: "Calibri", valign: "middle"
}});
s6.addText("{jstr(safe(da.get('access_point')))}", {{
  x: 6.6, y: 4.75, w: 2.8, h: 0.55,
  fontSize: 9, color: C.textMid, fontFace: "Calibri", valign: "middle", wrap: true
}});

// ─────────────────────────────────────────────────────────────────────────────
// Write file
// ─────────────────────────────────────────────────────────────────────────────
pres.writeFile({{ fileName: "{output_path}" }})
  .then(() => console.log("Slides written to {output_path}"))
  .catch(err => {{ console.error(err); process.exit(1); }});
"""
    return js


def main():
    parser = argparse.ArgumentParser(description="Convert pQTL reviewer JSON to PPTX slides")
    parser.add_argument("input_json", help="Path to JSON file from pQTL Olink reviewer")
    parser.add_argument("output_pptx", nargs="?", help="Output .pptx path (default: same as input with .pptx)")
    parser.add_argument("--pdf", action="store_true", help="Also convert to PDF")
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"Error: {args.input_json} not found", file=sys.stderr)
        sys.exit(1)

    data = load_json(args.input_json)

    base = os.path.splitext(args.input_json)[0]
    out_pptx = args.output_pptx or (base + ".pptx")

    js_code = build_js(data, out_pptx)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, dir="/tmp") as f:
        f.write(js_code)
        js_path = f.name

    # Find global node_modules so the temp script can require pptxgenjs
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = os.environ.copy()
    env["NODE_PATH"] = npm_root

    try:
        result = subprocess.run(
            ["node", js_path],
            capture_output=True, text=True, env=env
        )
        if result.returncode != 0:
            print("Node.js error:", result.stderr, file=sys.stderr)
            sys.exit(1)
        print(result.stdout.strip())
    finally:
        os.unlink(js_path)

    if args.pdf:
        pdf_path = os.path.splitext(out_pptx)[0] + ".pdf"
        soffice_script = os.path.join(os.path.dirname(__file__), "../../../skills/public/pptx/scripts/office/soffice.py")
        if os.path.exists(soffice_script):
            subprocess.run(["python", soffice_script, "--headless", "--convert-to", "pdf", out_pptx], check=True)
            print(f"PDF written to {pdf_path}")
        else:
            print("PDF conversion: run 'python scripts/office/soffice.py --headless --convert-to pdf <pptx>'")

    print(f"Done → {out_pptx}")


if __name__ == "__main__":
    main()
