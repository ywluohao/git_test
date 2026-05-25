# OBJECTIVE

Review ALL files available in the connected OneDrive Business location and create a complete, source-traceable Audit Approval Authority Matrix.

This is a document-review task, NOT a summarization task.

Use ONLY explicit statements found in source documents.

Do NOT use assumptions, common audit practice, inferred ownership, or outside knowledge.

---

# EXECUTION MODE

Perform the work in the following internal phases during ONE execution.

Do NOT stop between phases.

Do NOT request confirmation between phases.

Process files sequentially.

Do NOT sample files.

Do NOT skip files because they appear repetitive or irrelevant.

Continue until:

Total Files Processed + Total Files Failed = Total Files Discovered

---

# PHASE 1 — DISCOVER + INVENTORY + CLASSIFY

For EVERY file capture:

| File Name | File Type | Folder Path | Read Status | Category | Authoritative | Included in Analysis | Reason |

Read Status values:

- Processed
- Failed to Read
- Empty / No Content

Categories:

1 = Methodology / Standards / Policy
(authoritative)

2 = Procedures / Process documents
(supporting)

3 = Templates / Forms
(non-authoritative)

4 = Guides / Training / Notes
(non-authoritative)

Authority rules:

Category 1:
Primary authority

Category 2:
Supporting only if explicitly tied to Category 1

Category 3:
Not authority

Category 4:
Not authority

Templates cannot become authority unless explicitly supported by methodology documentation.

---

# PHASE 2 — EXTRACT APPROVAL RULES

Analyze ONLY files where:

Included in Analysis = Y

Search for:

approve
approval
sign-off
authorize
review required
must review
must approve
escalation
exception
override
scope change
rescope
rating override
major rating
sensitive report
issue severity
sampling approach
closure approval
audit planning memo
high-risk engagement
compensating controls

For EACH finding capture:

| Source File | Section | Page | Exact Wording | Approval Action | Owner | Confidence |

Owner mapping:

AM:

- prepare
- draft
- execute

SAM:

- review
- approve

Director:

- approve
- escalation
- override
- exception

If ownership is not explicitly defined:

Confidence = Low

Never infer.

---

# PHASE 3 — GROUP BY AUDIT LIFECYCLE

Group findings exactly:

- Pre-Planning
- Planning
- Fieldwork
- Reporting
- Issue Follow-Up / Closure

---

# PHASE 4 — BUILD AUDIT APPROVAL AUTHORITY MATRIX

Create:

| Stage | Deliverable | AM Authority | SAM Authority | Director Authority | Escalation Trigger | Source File | Exact Location | Confidence |

Rules:

- Every row must have source
- Multiple sources must all be listed
- Preserve exact wording
- Undefined items:

Source:
"Not explicitly defined"

Confidence:
Low

---

# PHASE 5 — CREATE SWIMLANE SUMMARY

| Stage | AM Responsibility | SAM Responsibility | Director Responsibility | Source |

---

# PHASE 6 — IDENTIFY GAPS

Identify:

- Missing approvals
- Conflicting rules
- Ambiguous language
- Missing ownership

Create:

| Description | Impact | Source | Recommendation |

Recommendations must be clearly marked as recommendations.

---

# PHASE 7 — FILE TRACEABILITY INDEX

Create:

| File Name | Used In Matrix | Used In Swimlane | Used In Gaps | Notes |

Include ALL files.

---

# QUALITY CHECKS

Before finalizing verify:

□ Total discovered = processed + failed

□ No files skipped

□ Templates not treated as authority

□ No assumptions made

□ Every matrix row has source

□ Multiple sources merged

□ Exact wording preserved

---

# FINAL OUTPUT ORDER

1. Coverage Summary
2. File Inventory
3. Audit Approval Authority Matrix
4. Swimlane Summary
5. Gaps & Decisions Needed
6. File Traceability Index

Coverage Summary:

Total Files Discovered:
Total Files Processed:
Total Files Failed:
Total Files Used:
Coverage Status:

Save final output as:

Audit_Approval_Authority_Matrix.md