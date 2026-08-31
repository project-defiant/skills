# Read publication

Atomic read-only task for extracting usable text from one local PDF. It does not access the Wiki, create notes, summarize content, or identify topics.

## Function

```text
read-publication(publication_path)
```

## Task

Read the PDF in reading order using the PDF skill and available PDF tooling. Use `pypdf` or `pdfplumber` first. If the PDF has no usable text, use OCR. Return the extracted text only.

Do not add page markers, page references, annotations, highlights, or inferred content. Fail if neither text extraction nor OCR produces usable text.

## Output

Return plain extracted text. This output is passed unchanged to `summarize-publication` and `extract-topics` so the PDF is read only once.
