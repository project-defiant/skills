---
name: pqtl-olink-reviewer
description: >
  Use this skill whenever a user wants to review, extract data from, or summarize a pQTL
  (protein quantitative trait loci) publication that uses Olink proteomics data. Triggers
  include: any mention of "pQTL paper", "Olink study", "proteogenomics review",
  "extract data from pQTL", "summarize pQTL publication", "literature database entry for
  proteomics", or when a user uploads or pastes content from a pQTL/Olink GWAS paper and
  asks for structured extraction or summarization. Also use when the user mentions
  specific Olink pQTL studies (e.g. UKB-PPP, SCALLOP, deCODE, FinnGen proteomics) and
  wants structured data extracted. This skill covers both cis- and trans-pQTL studies,
  including multi-ancestry designs.
---

# pQTL Olink Publication Reviewer

A skill for extracting structured data from and summarizing pQTL publications that use
Olink proteomics platforms. Designed for computational/statistical geneticists building
literature databases.

## What This Skill Produces

For each paper, produce **three outputs** in this order:
1. A **structured narrative** with clearly labeled sections
2. A **markdown table** of all extracted fields
3. A **JSON object** for programmatic database ingestion

See `references/output-templates.md` for exact templates and field specifications.
See `references/field-guide.md` for detailed extraction guidance per field.

---

## Extraction Domains

Work through all seven domains below. For every field:
- If clearly reported → extract and record it
- If not reported → use `null` in JSON, omit from markdown table, and add a brief note
  in the narrative Quality Concerns section explaining what was missing and why it matters

---

### DOMAIN 1: Study Identity & Design

Extract:
- **Paper title, authors, journal, year, DOI**
- **Cohort name(s)** (e.g. UKB-PPP, SCALLOP, deCODE, FinnGen, INTERVAL)
- **Total sample size** (N)
- **Study design** (cross-sectional, longitudinal, case-control, biobank)
- **Sample matrix** (plasma, serum, CSF, other)
- **Ancestry groups included** — list all ancestries, per-ancestry N
- **Whether multi-ancestry analyses were run jointly or separately**
- **Whether ancestry-specific pQTLs were reported**, and if so how many

---

### DOMAIN 2: Olink Platform & Proteomics QC

Extract:
- **Olink panel name and version** (e.g. Explore 3072, Explore 1536, Target 96 Inflammation)
- **Total number of proteins assayed**
- **Number of proteins with at least one significant pQTL**
- **NPX normalization approach**: batch/plate correction method used
- **Intensity/quantile normalization**: whether applied and how described
- **LOD (Limit of Detection) handling**: how below-LOD samples were treated (excluded,
  imputed, set to LOD/√2, etc.), and what % below-LOD threshold was applied per protein
- **Bridging normalization** (for multi-cohort/multi-batch studies):
  - Whether performed (yes/no)
  - Number of bridge samples used
  - Which dataset was used as the reference

---

### DOMAIN 3: Genotyping & Imputation

Extract:
- **Genotyping array(s)** used
- **Imputation reference panel** (e.g. HRC, TOPMed, 1000 Genomes)
- **Imputation R² quality threshold** used for variant filtering
- **MAF threshold** applied, and note whether this seems appropriate given sample size
  (e.g. MAF < 0.01 in N < 1,000 yields very few minor allele carriers and is likely
  underpowered; MAF < 0.001 is only appropriate for very large biobanks N > 30,000)

---

### DOMAIN 4: GWAS Methodology

Extract:
- **Statistical model** (e.g. linear regression via PLINK, BOLT-LMM, SAIGE, REGENIE)
- **Significance threshold(s)**:
  - Genome-wide threshold used (e.g. 5×10⁻⁸)
  - Whether an additional Bonferroni correction for number of proteins was applied
  - Whether separate thresholds were used for cis vs trans
- **cis/trans window definition**:
  - Exact window size (e.g. ±500kb, ±1Mb, ±2Mb)
  - Anchor point (TSS, gene body start, gene body end)
- **Full covariate list** as reported (e.g. age, sex, BMI, top N genetic PCs, PEER
  factors, batch, plate, disease status, medications, fasting status)

---

### DOMAIN 5: Post-GWAS Analyses

Extract:
- **Fine-mapping**:
  - Method used (e.g. COJO, SuSiE, FINEMAP, CAVIARBF)
  - Key outputs: number of credible sets reported, PIP threshold used
- **Colocalization**:
  - Method used (e.g. coloc, eCAVIAR, HyPrColoc)
  - Traits/datasets tested against (e.g. eQTL datasets, specific GWAS disease loci)
  - PP4 threshold used
  - Key findings: which proteins colocalized with which disease loci
- **Epitope-binding artifact assessment** (Olink-specific):
  - Whether the study tested for cis-pQTLs driven by SNPs in the antibody epitope region
  - Method used (e.g. comparison with SomaScan, mass spectrometry, clinical immunoassays)
  - Number of cis-pQTLs flagged or excluded as potential epitope artifacts
- **Trans-pQTL hotspot analysis**:
  - Key hotspot loci reported (e.g. ABO, HLA, APOE, FUT2)
  - Number of proteins influenced by each hotspot

---

### DOMAIN 6: Mendelian Randomization

Extract:
- Whether MR analyses were performed (yes/no)
- Which proteins were tested as exposures
- Which outcomes were tested
- MR methods used (e.g. IVW, MR-Egger, weighted median, MR-PRESSO)
- Whether F-statistics were reported for instrument strength
- Key MR findings (significant protein-outcome causal pairs)

---

### DOMAIN 7: Data Availability

Extract:
- Whether GWAS summary statistics are publicly available (yes/no)
- Specific access point: GWAS Catalog accession ID, URL, or controlled-access portal
  (e.g. UK Biobank RAP, dbGaP accession, Synapse ID)

---

## Output Instructions

After extracting all fields, produce outputs in this order:

### Output 1: Structured Narrative

Use these section headers exactly:

```
## [Paper Title] — Structured Review

### 1. Study Identity & Design
### 2. Olink Platform & Proteomics QC
### 3. Genotyping & Imputation
### 4. GWAS Methodology
### 5. Post-GWAS Analyses
### 6. Mendelian Randomization
### 7. Data Availability
### 8. Quality Concerns
```

For Section 8 (Quality Concerns), list as bullet points any fields that were not
reported, with a one-sentence note on why each matters for a computational geneticist.
If no concerns, write "No major quality concerns identified."

### Output 2: Markdown Table

Two-column table: `| Field | Value |`. Include only fields that were successfully
extracted. Omit null/not-reported fields. Group rows by domain using bold section
labels (e.g. **Study Design**, **Platform QC**, etc.).

### Output 3: JSON Object

Follow the schema in `references/output-templates.md`. Use `null` for unreported fields.
All field names in snake_case. Wrap in a fenced ```json code block.

---

## Key Concepts Reference

For quick reference when reading papers:

- **NPX**: Normalized Protein eXpression — Olink's log₂-scale relative abundance unit.
  Each +1 NPX ≈ 2-fold increase in protein level. Not an absolute concentration.
- **LOD**: Limit of Detection — the lowest signal distinguishable from background noise.
  Proteins with many samples below LOD may have distorted GWAS distributions.
- **Bridging normalization**: When combining data from multiple Olink batches/runs,
  shared "bridge samples" run across batches allow cross-batch NPX harmonization.
- **cis-pQTL**: Genetic variant associated with a protein encoded by a nearby gene
  (within the defined cis window, typically ±1Mb of TSS).
- **trans-pQTL**: Genetic variant associated with a protein encoded by a distant gene
  (outside the cis window).
- **Epitope artifact**: A cis-pQTL driven by a SNP that alters antibody binding to
  the protein (not true protein level change) — an Olink-specific technical concern.
- **PIP**: Posterior Inclusion Probability from fine-mapping — probability that a
  variant is the causal variant. PIP ≥ 0.9 = high-confidence causal variant.
- **PP4**: Posterior probability of colocalization — probability that a pQTL and a
  GWAS signal share the same causal variant. PP4 > 0.8 typically considered strong.

For full field definitions and extraction edge cases, read `references/field-guide.md`.
