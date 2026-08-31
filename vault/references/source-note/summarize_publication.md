# Summarize publication

Atomic publication-summary task. It consumes text already extracted by `read-publication`; it does not read the PDF, access the Wiki, create notes, annotate files, or make workflow decisions.

## Function

```text
summarize-publication(metadata, publication_text)
```

## Task

Write Markdown containing exactly these sections:

```markdown
## Research Question

## Study Design

## Key Findings

## Limitations

## Conclusions
```

Use only the supplied publication text. If information is absent, write `Not reported`. Do not infer, invent, add page references, or add PDF highlight links.

## Output

Return the Markdown body only. Frontmatter and file creation belong to `create-source-note`.
