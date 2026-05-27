# Audit Accountability Workflow

## RESET INSTRUCTIONS

Ignore all previous conversation context.

Ignore all previous inventories.

Ignore all previous assumptions.

Ignore all previous findings.

Ignore all previous accountability determinations.

Ignore all previous uploaded files.

Ignore prior thread memory.

Use ONLY:

master_input.md

Treat the uploaded file as the sole source of truth.

Do not use information from previous sessions.

If information is not found:

write:

Not found in provided source

---

## Objective

Analyze all methodology content contained in master_input.md and determine audit accountability across the audit lifecycle.

Use methodology evidence first.

Do not use external knowledge.

Do not invent ownership.

Do not invent objectives.

Use the predefined audit objective framework below as the primary structure.

All document scanning must align to this framework.

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

Do NOT reopen original files.

---

# Execution Order

Stage 0 → Inventory

Stage 1 → Build Audit Objective Framework

Stage 2 → Scan Files Against Audit Objectives

Stage 3 → Identify AM/SAM/Director Involvement

Stage 4 → Accountability Determination

Stage 5 → Generate Swimlane

Stage 6 → Final Validation

---

# Stage 0 — Build Complete File Inventory

```text
Objective:

Build complete inventory.

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

# Stage 1 — Build Audit Objective Framework

```text
Objective:

Use the following audit objectives as the canonical structure.

Do not create new objectives unless explicitly required.

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

| Audit Stage | Objective |
```

---

# Stage 2 — Scan Files Against Audit Objectives

```text
Objective:

Process all files using the audit objective framework above.

For each objective:

Search for:

• activities
• deliverables
• reviews
• approvals
• sign-offs
• escalations
• mandatory actions
• meetings
• communications
• ownership references
• responsibilities
• role interactions

Capture exact wording only.

Do not infer.

If no evidence exists:

mark:

Not found in provided source

Output:

| Audit Stage | Objective | Activity/Event | Exact Language | Source |
```

---

# Stage 3 — Identify AM/SAM/Director Involvement

```text
Objective:

For every activity/event:

Identify any AM/SAM/Director involvement.

Search for:

• perform
• prepare
• review
• approve
• discuss
• attend
• notify
• escalate
• communicate
• validate
• challenge
• monitor
• document
• assign
• delegate
• sign
• conclude
• own
• participate
• coordinate
• lead
• present
• finalize
• track
• follow up

Capture exact wording only.

Do not infer.

Output:

| Audit Stage | Objective | Event | Role | Exact Language | Source |
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

Explicit ownership:

Confidence = High

Role implied through wording:

Confidence = Medium

Role inferred through process sequence:

Confidence = Low

Status:

Recommended assumption

No evidence:

Status:

Not found

Output:

| Audit Stage | Objective | Event | AM | SAM | Director | Confidence | Evidence | Source |
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

Generate using ONLY Stage 4 output.

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
• Objectives without activities
• Activities without ownership
• Ownership without evidence
• Unsupported assumptions

Final:

Did all files get processed?

YES / NO

If NO:

List missing items.
```