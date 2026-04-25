# Field Extraction Guide

Detailed extraction rules and edge cases for each field in the pQTL Olink reviewer.

---

## Study Design Fields

### Ancestry groups
- List all ancestries exactly as described in the paper (e.g. "European", "British/Irish",
  "South Asian", "African", "East Asian", "Hispanic/Latino")
- If a paper says "predominantly European" without per-ancestry N breakdown, record the
  ancestry as described and note in Quality Concerns that per-ancestry N was not reported
- For multi-ancestry studies, always capture whether the GWAS was run:
  - **Jointly**: all ancestries in one model with ancestry as covariate or PCs
  - **Separately**: per-ancestry GWAS then meta-analysed
  - **Both**: separate runs + joint meta-analysis

### Study design types
Use one of: `cross-sectional`, `longitudinal`, `case-control`, `population-biobank`,
`clinical-cohort`, `meta-analysis`, `consortium`

---

## Olink Platform Fields

### Panel identification
Common panels to recognize:
- **Explore 3072** / **Explore 3K**: ~3,000 proteins, 8 sub-panels, NGS readout
- **Explore 1536** / **Explore 1.5K**: ~1,500 proteins, 4 sub-panels, NGS readout
- **Explore HT** / **Explore 5K**: ~5,400 proteins, newest generation
- **Target 96**: 92 proteins per panel (e.g. Target 96 Inflammation, Cardiovascular II),
  qPCR readout
- **Focus**: custom small panels

If a paper only says "Olink" without specifying the panel, record as "Not specified" and
note in Quality Concerns.

### NPX batch/plate correction
Look for mentions of:
- Inter-plate control (IPC) normalization
- Bridge sample normalization
- ComBat batch correction
- Median centering
- Intensity normalization (used when many plates, assumes randomized samples)

### LOD handling
Common approaches papers describe:
- Exclude samples below LOD (record threshold: e.g. >20% below LOD → protein excluded)
- Set to LOD/2 or LOD/√2
- Include as-is with warning
- Use the `OlinkAnalyze` R package LOD functions

If a paper excludes proteins where >X% of samples are below LOD, record X as
`lod_exclusion_threshold_pct`.

### Bridging normalization edge cases
- Some papers use "reference samples" or "QC samples" — these are bridge samples
- If a paper mentions combining Olink batches or cohorts but doesn't mention bridging,
  note this as a Quality Concern (cross-batch comparability may be compromised)
- The reference dataset is typically the larger or earlier dataset

---

## Genotyping & Imputation Fields

### Imputation reference panels — common ones:
- **HRC** (Haplotype Reference Consortium): ~65M variants, European-focused
- **TOPMed**: ~300M variants, more diverse ancestry coverage
- **1000 Genomes Phase 3**: older, less dense but widely used
- **UK Biobank imputation panel**: HRC + UK10K, used in UKB studies
- **gnomAD**: sometimes used as reference for rare variant analyses

### MAF appropriateness note
Apply this rough guidance:
- N < 1,000: MAF < 0.05 yields very few minor allele carriers — note as potentially
  underpowered for common variant detection
- N 1,000–10,000: MAF < 0.01 is borderline — note if used
- N > 10,000: MAF < 0.001 becomes feasible for well-powered rare variant discovery
- N > 50,000: MAF as low as 0.0001 may be appropriate

---

## GWAS Methods Fields

### Statistical model identification
Look for these keywords:
- `PLINK`, `PLINK2`: standard linear regression, doesn't account for relatedness
- `BOLT-LMM`: linear mixed model, handles relatedness well, fast for large N
- `SAIGE`: logistic/linear mixed model, handles case-control imbalance
- `REGENIE`: whole-genome regression, handles large biobanks and relatedness
- `GEMMA`, `EMMAX`: older LMMs

### Significance thresholds — what to look for
Papers often use layered thresholds:
1. Genome-wide: 5×10⁻⁸ (standard GWAS)
2. Protein-level Bonferroni: 5×10⁻⁸ / N_proteins (e.g. for 3,000 proteins:
   5×10⁻⁸ / 3,000 ≈ 1.67×10⁻¹¹)
3. Separate cis/trans thresholds: some papers use lenient cis (e.g. 1×10⁻⁶) and
   strict trans (e.g. 5×10⁻⁸ or stricter)

Always record thresholds as strings (e.g. "5e-8", "1.67e-11") to preserve precision.

### cis window anchor points
- **TSS** (Transcription Start Site): most common for eQTL-style analyses
- **Gene body**: ±window from both ends of the gene
- **Midpoint**: center of the gene — less common
- If not specified, record anchor as null and note in Quality Concerns

### Covariates — what to look for
Common covariate categories to scan for in methods:
- **Demographic**: age, sex, age², age×sex interaction
- **Anthropometric**: BMI, weight, height
- **Population stratification**: top N genetic principal components (note how many)
- **Technical proteomics**: plate ID, batch, assay lot, Olink run
- **Clinical**: disease status, medication use, fasting status, smoking, alcohol
- **Other omics**: PEER factors, hidden confounders (HCP)

Record the full list as an array of strings exactly as described.

---

## Post-GWAS Fields

### Fine-mapping methods
- **COJO** (Conditional and Joint analysis): identifies independent signals via
  stepwise conditional regression; part of GCTA software
- **SuSiE** (Sum of Single Effects): Bayesian fine-mapping producing credible sets
- **FINEMAP**: Bayesian fine-mapping, outputs PIPs per variant
- **CAVIARBF**: similar Bayesian approach
- Some papers do manual conditional analysis (condition on lead SNP, re-run GWAS)

Key outputs to extract:
- Number of credible sets (SuSiE) or independent signals (COJO) reported
- PIP threshold used to define "putative causal" variants (typically PIP ≥ 0.9 or 0.95)

### Colocalization — traits tested
Look for:
- eQTL datasets: GTEx (specify tissue), eQTLGen (blood), BrainSeq, etc.
- Disease GWAS: specific traits (e.g. CAD, T2D, IBD, Alzheimer's) and their sources
- Other pQTL datasets used for cross-platform comparison

PP4 (posterior probability of colocalization, H4) threshold:
- PP4 > 0.8: strong evidence for shared causal variant (most common threshold)
- PP4 > 0.5: suggestive colocalization
- Record whatever threshold the paper uses

### Epitope-binding artifact assessment
This is critical for Olink interpretation. A cis-pQTL where the associated SNP falls
within the epitope region recognized by the Olink antibody may reflect:
- The SNP changing antibody binding (assay artifact) rather than true protein level change
- This can create false positive cis-pQTLs or distorted effect sizes

Methods papers use to detect these:
1. Cross-platform comparison: does the same cis-pQTL replicate in SomaScan or MS data?
   Non-replication suggests epitope artifact
2. Coding variant annotation: is the SNP a missense variant in the protein coding region?
3. Structural analysis: does the SNP fall in a known antibody binding domain?

Record n_pqtls_flagged as the number excluded or flagged (not just tested).

### Trans-pQTL hotspots
Common hotspot loci seen in Olink pQTL papers — recognize these by name:
- **ABO**: blood group locus, affects glycosylation of many plasma proteins
- **HLA**: major histocompatibility complex, affects immune proteins
- **APOE/APOC1**: lipid metabolism, affects many cardiovascular proteins
- **FUT2**: fucosyltransferase, affects glycan-modified proteins
- **IGHG**: immunoglobulin heavy chain region

Record each hotspot locus name and the number of proteins it influences as a trans-pQTL.

---

## MR Fields

### MR instrument selection
Papers often describe how they selected genetic instruments (IVs) for MR:
- Typically use cis-pQTLs as instruments (strongest evidence, fewest pleiotropy concerns)
- Sometimes use all pQTLs (cis + trans)
- Note whether instruments were clumped/pruned for LD

### MR methods glossary
- **IVW** (Inverse Variance Weighted): main MR method, assumes no directional pleiotropy
- **MR-Egger**: allows for pleiotropy, less precise
- **Weighted median**: robust if ≤50% of instruments are invalid
- **MR-PRESSO**: detects and removes outlier instruments
- **Steiger filtering**: removes instruments where variant explains more outcome variance
  than exposure variance

### F-statistic
Measure of instrument strength. F > 10 is conventional threshold for "strong instrument."
Note whether F-statistics are reported per protein or as a summary.

---

## Data Availability Fields

### Common access points to recognize
- **GWAS Catalog**: accession IDs start with "GCST" (e.g. GCST90000001)
- **UK Biobank RAP**: controlled access via DNAnexus platform
- **Synapse**: IDs start with "syn" (e.g. syn51364943)
- **dbGaP**: accession IDs start with "phs" (e.g. phs000007)
- **Zenodo**: open DOI-based repository
- **FigShare**: open repository
- **EMBL-EBI**: European data archive
- **deCODE**: often via application to deCODE Genetics directly

Record the exact accession number or URL wherever possible.
