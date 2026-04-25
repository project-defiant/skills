# Output Templates

## JSON Schema

```json
{
  "paper": {
    "title": "string",
    "authors": "string",
    "journal": "string",
    "year": "integer",
    "doi": "string"
  },
  "study_design": {
    "cohort_names": ["string"],
    "total_n": "integer",
    "design_type": "string",
    "sample_matrix": "string",
    "ancestries": [
      {
        "group": "string",
        "n": "integer"
      }
    ],
    "multi_ancestry_analysis": "joint | separate | null",
    "ancestry_specific_pqtls_reported": "boolean | null",
    "n_ancestry_specific_pqtls": "integer | null"
  },
  "olink_platform": {
    "panel_name": "string",
    "panel_version": "string",
    "n_proteins_assayed": "integer",
    "n_proteins_with_pqtl": "integer | null",
    "npx_batch_correction_method": "string | null",
    "npx_intensity_normalization": "string | null",
    "lod_handling": "string | null",
    "lod_exclusion_threshold_pct": "number | null",
    "bridging_performed": "boolean | null",
    "n_bridge_samples": "integer | null",
    "bridging_reference_dataset": "string | null"
  },
  "genotyping": {
    "array": "string | null",
    "imputation_reference_panel": "string | null",
    "imputation_r2_threshold": "number | null",
    "maf_threshold": "number | null",
    "maf_appropriateness_note": "string | null"
  },
  "gwas_methods": {
    "statistical_model": "string | null",
    "significance_threshold_genomewide": "string | null",
    "bonferroni_correction_for_proteins": "boolean | null",
    "cis_threshold": "string | null",
    "trans_threshold": "string | null",
    "cis_window_size_kb": "integer | null",
    "cis_window_anchor": "TSS | gene_body | gene_end | null",
    "covariates": ["string"]
  },
  "post_gwas": {
    "fine_mapping": {
      "performed": "boolean",
      "method": "string | null",
      "n_credible_sets": "integer | null",
      "pip_threshold": "number | null"
    },
    "colocalization": {
      "performed": "boolean",
      "method": "string | null",
      "traits_tested": ["string"],
      "pp4_threshold": "number | null",
      "key_findings": "string | null"
    },
    "epitope_artifact_assessment": {
      "performed": "boolean",
      "method": "string | null",
      "n_pqtls_flagged": "integer | null"
    },
    "trans_hotspots": [
      {
        "locus": "string",
        "n_proteins_influenced": "integer"
      }
    ]
  },
  "mendelian_randomization": {
    "performed": "boolean",
    "proteins_tested": ["string"],
    "outcomes_tested": ["string"],
    "methods_used": ["string"],
    "f_statistics_reported": "boolean | null",
    "key_findings": "string | null"
  },
  "data_availability": {
    "summary_stats_public": "boolean | null",
    "access_point": "string | null"
  }
}
```

---

## Markdown Table Template

```markdown
| Field | Value |
|-------|-------|
| **Study Design** | |
| Cohort(s) | |
| Total N | |
| Design type | |
| Sample matrix | |
| Ancestries (N per group) | |
| Multi-ancestry analysis | |
| Ancestry-specific pQTLs | |
| **Olink Platform & QC** | |
| Panel name & version | |
| Proteins assayed | |
| Proteins with ≥1 pQTL | |
| Batch/plate correction | |
| Intensity normalization | |
| LOD handling | |
| LOD exclusion threshold | |
| Bridging performed | |
| Bridge samples (N) | |
| Bridging reference dataset | |
| **Genotyping & Imputation** | |
| Genotyping array | |
| Imputation reference panel | |
| Imputation R² threshold | |
| MAF threshold | |
| MAF appropriateness note | |
| **GWAS Methods** | |
| Statistical model | |
| Genome-wide threshold | |
| Protein Bonferroni correction | |
| cis threshold | |
| trans threshold | |
| cis window size | |
| cis window anchor | |
| Covariates | |
| **Post-GWAS** | |
| Fine-mapping method | |
| Fine-mapping: credible sets | |
| Fine-mapping: PIP threshold | |
| Colocalization method | |
| Colocalization traits tested | |
| Colocalization PP4 threshold | |
| Colocalization key findings | |
| Epitope artifact assessment | |
| Epitope artifact method | |
| pQTLs flagged as epitope artifacts | |
| Trans hotspot loci | |
| **Mendelian Randomization** | |
| MR performed | |
| Proteins as exposures | |
| Outcomes tested | |
| MR methods | |
| F-statistics reported | |
| Key MR findings | |
| **Data Availability** | |
| Summary stats public | |
| Access point | |
```

Omit any row where the value is not reported. Add extracted values in the right column.
