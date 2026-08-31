# Extract publication metadata

Isolated read-only publication-metadata task used by publication workflows. Use the PDF skill and PDF tooling for this task; do not use Obsidian CLI to read the publication.

This task extracts bibliographic facts from the supplied publication. It does not access the Wiki, create wikilinks, create notes, or make workflow decisions.

## Function

```text
extract-publication-metadata(publication_path)
```

- `publication_path`: path to the publication supplied by the user.

## Preconditions

- `publication_path` points to a readable local PDF.
- PDF tooling is available: `pypdf` or `pdfplumber`; use `pdfinfo` when available for document-level metadata.
- This task does not require an Obsidian vault.

## Task

Read the PDF with `pypdf` or `pdfplumber`, inspect its embedded metadata and publication text, and return the available bibliographic metadata as JSON. Use `pdfinfo` for basic document metadata when available:

```bash
pdfinfo "$publication_path"
```

Do not treat embedded PDF metadata as authoritative when the publication text provides a more precise value. Do not infer or invent missing bibliographic values.

Return:

- `title`: exact full publication title.
- `authors`: all available authors, in publication order.
- `year`: publication year.
- `publication_date`: full publication date when available.
- `journal`: journal title.
- `doi`: DOI when available.
- `pmid`: PubMed ID when available.
- `url`: canonical publication or DOI URL when available.
- `source_path`: the supplied publication path.
- `source_key`: `{last_author} {year}`, using the final listed author surname, for source-note lookup and naming.

Omit unavailable bibliographic fields rather than inventing values. Preserve `source_path` exactly. Do not shorten or paraphrase the publication title.

## Output schema

```json
{
  "type": "object",
  "required": ["title", "source_path", "source_key"],
  "properties": {
    "title": { "type": "string", "minLength": 1 },
    "authors": {
      "type": "array",
      "items": { "type": "string" }
    },
    "year": { "type": "integer" },
    "publication_date": { "type": "string" },
    "journal": { "type": "string" },
    "doi": { "type": "string" },
    "pmid": { "type": "string" },
    "url": { "type": "string" },
    "source_path": { "type": "string", "minLength": 1 },
    "source_key": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```
