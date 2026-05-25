# OBJECTIVE

Review ALL files in the connected OneDrive Business location and create a complete document inventory.

This is NOT an analysis task.

Do NOT summarize content.

Do NOT extract approval rules yet.

Your only goal is to discover, read, classify, and track every file.

---

# EXECUTION RULES

Process files sequentially.

Read files one by one.

Do NOT sample files.

Do NOT skip files because they appear duplicate, repetitive, or irrelevant.

Continue until:

Total Files Processed + Total Files Failed = Total Files Discovered

---

# For EVERY file capture:

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

Authoritative values:

- Yes
- Maybe
- No

Rules:

Category 1:
Primary authority

Category 2:
Supporting only if explicitly tied to Category 1

Category 3:
Not authority

Category 4:
Not authority

If Included in Analysis = N:

Reason is mandatory.

---

# COVERAGE SUMMARY

Provide:

Total Files Discovered:
Total Files Processed:
Total Files Failed:
Total Files Included:
Coverage Status:

If any file failed:

Coverage Status = Partial Coverage

---

# FINAL OUTPUT

Output markdown only.

Save as:

Audit_File_Inventory.md