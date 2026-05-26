# Audit Accountability Workflow

## Objective

Analyze all methodology content contained in master_input.md and determine audit accountability across the audit lifecycle.

Use methodology evidence first.

Do not use external knowledge.

Do not invent ownership.

If methodology does not explicitly support ownership:

mark:

Recommended assumption

Evidence must always be traceable to source documents.

---

## Context

GitHub Copilot has already consolidated all PDF files into:

master_input.md

Treat:

# File Fxxx:

as individual source document boundaries.

Read ONLY:

master_input.md

Do NOT re-open original files.

---

# Execution Order

Stage 0 → Inventory

Stage 1 → Evidence Extraction

Stage 2 → Normalize Activities

Stage 3 → Map to Audit Stages/Objectives

Stage 4 → Accountability Determination

Stage 5 → Swimlane Generation

Stage 6 → Final Validation

---

# Stage 0 — Build Complete File Inventory

```text
Objective:

Build a complete inventory of all source documents.

Instructions:

1. Enumerate every:

# File Fxxx:

section

2. Return exact names

3. Assign IDs:

F001
F002
F003
...

Output:

| File ID | File Name |

Validation:

• Total files detected
• Total files indexed

STOP if files are not listed individually.
```

---

# Stage 1 — Evidence Extraction

```text
Objective:

Extract:

• Activities
• Deliverables
• Review requirements
• Approval requirements
• Sign-offs
• Escalation requirements
• Mandatory actions

Capture exact wording only.

Output:

| File ID | File | Page | Activity | Requirement Type | Exact Language | Source |

Validation:

• Files processed
• Missing files

STOP if count mismatch.
```

---

# Stage 2 — Normalize Activities

```text
Objective:

Normalize duplicate activities.

Do NOT merge:

review
approve
sign-off
authorize
perform
escalate

unless wording explicitly indicates identical actions.

Output:

| Standard Activity | Original Activity | Source |
```

---

# Stage 3 — Map to Audit Stages/Objectives

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

# Stage 4 — Accountability Determination

```text
Objective:

Determine:

AM
SAM
Director

Rules:

Use methodology evidence first.

Explicit ownership:

Confidence = High

Implied ownership:

Confidence = Medium

No supporting evidence:

Status = Recommended assumption

Output:

| Audit Stage | Objective | AM | SAM | Director | Approval Required | Confidence | Evidence | Source |
```

---

# Stage 5 — Generate Swimlane

```text
Objective:

Generate swimlane grouped by:

Pre-Planning
Planning
Fieldwork
Reporting
Issue Follow Up

For each:

AM
SAM
Director
```

---

# Stage 6 — Final Validation

```text
Validate:

• Total files detected
• Total files processed
• Missing files
• Objectives mapped
• Unsupported assumptions
• Activities without ownership
• Ownership without evidence

Final:

Did all files get processed?

YES / NO

If NO:

List missing files.
```