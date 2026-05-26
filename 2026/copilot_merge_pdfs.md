# GitHub Copilot Prompt — Merge PDF Methodology Files into One Markdown Source

## Role

You are working in VS Code Agent mode.

Use local workspace files only.

Do not use external knowledge.

Do not perform audit analysis in this step.

---

## Root Folder

```text
C:\Users\hluo04\OneDrive - BMO Financial Group\_shared\Corporate Audit SharePoint - Methodology (1ADM60 MAX 7 Years)
```

---

## Output Folder

Create the following folder if it does not exist:

```text
./output
```

---

## Objective

Recursively find all PDF methodology files and merge their extracted text into one consolidated Markdown file:

```text
./output/master_input.md
```

This file will later be uploaded to Copilot Research Agent for audit accountability analysis.

This task is only for source consolidation.

Do not classify files.

Do not extract findings.

Do not determine accountability.

Do not summarize.

Do not infer missing information.

---

## Scope

Process PDF files only.

Ignore:

- DOCX
- XLSX
- PPTX
- CSV
- images
- other non-PDF files

Do not attempt to read binary Office files.

Do not perform OCR.

Extract selectable PDF text only.

If a PDF has no selectable text, record that clearly.

---

# STEP 1 — PDF INVENTORY

Recursively find PDF files only.

Sort files alphabetically by relative path.

Assign File IDs:

```text
F001
F002
F003
...
```

Create:

```text
./output/00_pdf_inventory.csv
```

Columns:

```text
FileID,FileName,RelativePath,Readable,Status,Notes
```

Validation:

Return:

```text
Total PDFs detected
Total PDFs indexed
```

STOP if counts mismatch.

---

# STEP 2 — EXTRACT PDF TEXT

For each indexed PDF:

1. Open the PDF
2. Extract selectable text
3. Preserve page boundaries if available
4. Preserve exact wording as much as possible
5. Do not summarize
6. Do not rewrite
7. Do not infer missing text
8. Do not silently skip files

If extraction fails, still include the file in `master_input.md` with failure details.

---

# STEP 3 — CREATE MASTER MARKDOWN FILE

Create:

```text
./output/master_input.md
```

Use this exact structure:

```md
# Master PDF Extraction

Purpose:

This file consolidates selectable text extracted from PDF methodology files.

Later use:

Upload this file to Copilot Research Agent for audit accountability analysis.

Important rules:

- Each `# File Fxxx:` section is a separate source document.
- Source filename and relative path must be preserved.
- Page numbers must be preserved when available.
- Extraction failures must be recorded.
- No analysis has been performed in this file.

---

## File Index

| FileID | FileName | RelativePath | Status | Notes |
|---|---|---|---|---|

---

# File F001: filename.pdf

Source filename:
filename.pdf

Relative path:
relative/path/filename.pdf

Extraction status:
Extracted

Page count:
10

---

## Page 1

[exact extracted text]

---

## Page 2

[exact extracted text]

---

# File F002: another_file.pdf

Source filename:
another_file.pdf

Relative path:
relative/path/another_file.pdf

Extraction status:
Failed

Reason:
No selectable text found. OCR was not performed.

---
```

---

# STEP 4 — FINAL VALIDATION

Verify:

```text
PDFs detected = PDFs extracted successfully + PDFs failed
```

If mismatch exists, create:

```text
./output/missing_pdf_files.csv
```

Columns:

```text
FileID,FileName,RelativePath,ReasonMissing
```

At the end return only:

```text
Files detected: [number]
Files processed: [number]
Files failed: [number]
Output files created:
- ./output/00_pdf_inventory.csv
- ./output/master_input.md
- ./output/missing_pdf_files.csv, if applicable
Final status: YES/NO
```

Do not state completion until the output files are actually created.
