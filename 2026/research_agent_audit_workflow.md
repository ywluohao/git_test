# Copilot Research Agent Prompt — Audit Accountability Analysis from master_input.md

## Objective

Analyze all methodology content contained in `master_input.md` and determine audit accountability across the audit lifecycle.

Use methodology evidence first.

Do not use external knowledge.

Do not invent ownership.

If methodology does not explicitly support ownership, mark it as:

```text
Recommended assumption
```

Evidence must always be traceable to source documents.

---

## Input

Use only the uploaded file:

```text
master_input.md
```

Treat each section beginning with:

```text
# File Fxxx:
```

as one separate source document.

Do not ask for the original PDFs.

Do not re-open original files.

Do not use external sources.

---

# Execution Order

Stage 0 → Inventory  
Stage 1 → Classification  
Stage 2 → Evidence Extraction  
Stage 3 → Normalize Activities  
Stage 4 → Map to Audit Stages/Objectives  
Stage 5 → Accountability Determination  
Stage 6 → Swimlane Generation  
Stage 7 → Final Validation  

---

# Stage 0 — Build Complete File Inventory

```text
Objective:

Build a complete inventory of all source documents inside master_input.md.

Instructions:

1. Enumerate every `# File Fxxx:` section individually.
2. Return exact source filenames.
3. Preserve File IDs exactly as shown:

F001, F002, F003...

Output:

| File ID | File Name | File Type |

Validation:

• Total files detected
• Total files indexed

STOP if files are not listed individually.
```

---

# Stage 1 — File Classification

```text
Objective:

Classify all files.

Authority Levels:

Primary
- methodology
- standards
- policies
- audit charter
- process documents

Secondary
- templates
- checklists
- job aids
- supporting guidance

Reference
- examples
- best practices

Utility
- generators
- calculators
- tools

Templates cannot automatically be excluded.

Inspect templates for:

• sign-offs
• approvals
• reviewers
• workflow guidance
• ownership instructions

Output:

| File ID | File | Authority Level | Include | Reason |
```

---

# Stage 2 — Evidence Extraction

```text
Objective:

Extract methodology evidence from master_input.md.

Extract:

• Activities
• Deliverables
• Review requirements
• Approval requirements
• Sign-offs
• Escalation requirements
• Mandatory actions

Capture exact wording.

Do not summarize.

Do not paraphrase unless needed for the Activity column.

Output:

| File ID | File | Page | Activity | Requirement Type | Exact Language | Source |

Validation:

• Files processed
• Missing files

STOP if count mismatch.
```

---

# Stage 3 — Normalize Activities

```text
Objective:

Normalize duplicate activities.

Rules:

Normalize only true semantic duplicates.

Do NOT merge distinct control actions such as:

• review
• approve
• sign-off
• authorize
• perform
• escalate

unless the source wording clearly indicates the same action.

Output:

| Standard Activity | Original Activity | Source |
```

---

# Stage 4 — Map to Audit Stages/Objectives

```text
Objective:

Map activities into:

Pre-Planning
• Issue letter of engagement
• Confirm audit resources
• Engage audit analytics

Planning
• Finalize planning memorandum
• Finalize audit scope/program
• Finalize rating areas in MSI
• Prepare/send pull list

Fieldwork
• Kickoff meeting
• Execute/document/conclude testing
• Review work papers
• Discuss issues
• Ongoing meetings
• Draft issues

Reporting
• Draft report
• Closing meeting
• Publish report
• Close audit

Issue Follow Up
• Track issues
• Retest issues
• Close issues

Output:

| Audit Stage | Objective | Supporting Activities | Source |
```

---

# Stage 5 — Accountability Determination

```text
Objective:

Determine accountability for:

AM
SAM
Director

Rules:

1. Use methodology evidence first.

2. If the methodology explicitly assigns ownership:
   Confidence = High

3. If the methodology implies ownership through role language:
   Confidence = Medium

4. If the methodology is silent and ownership is inferred only from workflow logic:
   Status = Recommended assumption
   Confidence = Low

5. If there is no evidence and no reasonable support:
   Status = Not found

Output:

| Audit Stage | Objective | AM | SAM | Director | Approval Required | Confidence | Source |
```

---

# Stage 6 — Generate Swimlane

```text
Objective:

Generate swimlane grouped by:

Pre-Planning
Planning
Fieldwork
Reporting
Issue Follow Up

For each stage, show responsibilities for:

AM
SAM
Director

Use only Stage 5 accountability results.

Do not create new ownership conclusions in this stage.
```

---

# Stage 7 — Final Validation

```text
Validate:

• Total files detected
• Total files processed
• Missing files
• Objectives mapped
• Methodology conflicts
• Unsupported assumptions
• Activities without ownership
• Ownership without evidence

Final:

Did all files get processed?

YES / NO

If NO:

List missing files.
```

---

# Final Output Required

Return the final result with these sections:

```text
1. File Inventory Summary
2. File Classification Summary
3. Evidence Table
4. Normalized Activity List
5. Audit Stage / Objective Mapping
6. Accountability Matrix
7. Audit Authority Swimlane
8. Open Decisions
9. Validation Summary
```

Every finding must include source evidence.

If evidence is missing, write:

```text
Not found in provided source
```

If wording is unclear, write:

```text
Ambiguous
```
