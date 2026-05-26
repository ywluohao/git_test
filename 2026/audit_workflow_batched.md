
# Audit Accountability Workflow (Large File Set Version)

## Context
You have ~83 methodology artifacts (PDF, DOCX, PPTX, XLSX, templates, job aids, tools).

Do NOT ask Research Agent to read all files at once.
Use controlled batches.

---

# Execution Order

Stage 0 → Inventory  
Stage 1 → Classification  
Stage 2 → Evidence Extraction (batch processing)  
Stage 3 → Normalize Activities  
Stage 4 → Map to Audit Stages/Objectives  
Stage 5 → Accountability Determination  
Stage 6 → Swimlane Generation  
Stage 7 → Final Validation  

---

# Stage 0 — Build Complete File Inventory

```text
Objective:

Build a complete inventory of all files.

Instructions:

1. Enumerate every file individually
2. Return exact names
3. Assign IDs:
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

Secondary
- templates
- checklists
- job aids

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

# Stage 2 — Evidence Extraction (Batch Processing)

```text
Objective:

Read ONLY specified batch.

Example:

Read F001–F015 only.

Extract:

• Activities
• Deliverables
• Review requirements
• Approval requirements
• Sign-offs
• Escalation requirements
• Mandatory actions

Output:

| File | Activity | Requirement Type | Exact Language | Source |

Validation:

• Files processed
• Missing files

STOP if count mismatch.
```

Repeat batches:

Batch 1 → F001–F015
Batch 2 → F016–F030
Batch 3 → F031–F045
Batch 4 → F046–F060
Batch 5 → F061–F075
Batch 6 → F076–F083

---

# Stage 3 — Normalize Activities

```text
Normalize duplicate activities.

Output:

| Standard Activity | Original Activity | Source |
```

---

# Stage 4 — Map to Audit Stages/Objectives

```text
Map activities into:

Pre‑Planning
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
Determine:

AM
SAM
Director

Rules:

Use methodology evidence first.

If silent:

Mark:
Recommended assumption

Output:

| Audit Stage | Objective | AM | SAM | Director | Approval Required | Confidence | Source |
```

---

# Stage 6 — Generate Swimlane

```text
Generate swimlane grouped by:

Pre‑Planning
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

# Stage 7 — Final Validation

```text
Validate:

• Total files detected
• Total files processed
• Missing files
• Objectives mapped
• Methodology conflicts
• Unsupported assumptions

Final:

Did all files get processed?

YES / NO

If NO:

List missing files.
```
