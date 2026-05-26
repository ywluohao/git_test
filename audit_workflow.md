# Audit Accountability Analysis Workflow

## Objective

Analyze all methodology artifacts (\~83 files) and determine
accountability across audit stages/objectives while preserving
methodology evidence and traceability.

## Stage 0 --- File Discovery & Classification

**Goal:** Process all files and classify authority level.

Prompt:

``` text
Review every file.

Authority Levels:
- Primary: methodology, policies, standards, audit charter
- Secondary: templates, job aids, checklists
- Reference: examples, best practices
- Utility: generators, tools, macros

For each file determine:
1. Authority Level
2. Include Y/N
3. Reason

Inspect templates for:
- reviewer requirements
- sign-offs
- required approvals
- workflow instructions
- ownership guidance

Output:
| File | Authority Level | Include | Reason |

Validation:
- Total files detected
- Total files classified
- Missing files
- Duplicate files

STOP if processed count < detected count
```

------------------------------------------------------------------------

## Stage 1 --- Methodology Evidence Extraction

``` text
Read every included file.

Extract:
- Activities
- Deliverables
- Review requirements
- Approval requirements
- Sign-off requirements
- Escalation requirements
- Mandatory actions

Output:
| File | Activity | Requirement Type | Exact Language | Source |

Rules:
- Do not assign AM/SAM/Director
- Preserve conflicts
- Preserve duplicate references

STOP if processed count != included count
```

------------------------------------------------------------------------

## Stage 2 --- Normalize Activities

``` text
Normalize duplicate activities while preserving sources.

Output:
| Standard Activity | Original Activity | Source |
```

------------------------------------------------------------------------

## Stage 3 --- Map to Audit Stage / Objective Structure

``` text
Map into:

Pre‑Planning
- Issue letter of engagement
- Confirm audit resources
- Engage audit analytics

Planning
- Finalize planning memorandum
- Finalize audit scope and audit program
- Finalize rating areas in MSI
- Prepare/send pull list

Fieldwork
- Kickoff meeting
- Execute/document/conclude testing
- Review work papers
- Discuss issues with auditee
- Residual risk assessment

Reporting
- Draft audit report
- Closing meeting
- Publish report/issues
- Close audit

Issue Follow Up
- Track issues
- Retest issues
- Close issues

Output:
| Audit Stage | Objective | Supporting Activities | Source |
```

------------------------------------------------------------------------

## Stage 4 --- Accountability Determination

``` text
Determine accountability.

Roles:
AM
SAM
Director

Rules:
- Use methodology evidence first
- If silent: mark "Recommended assumption"

Output:
| Audit Stage | Objective | AM | SAM | Director | Approval Required | Confidence | Source |
```

------------------------------------------------------------------------

## Stage 5 --- Build Audit Authority Swimlane

``` text
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

------------------------------------------------------------------------

## Stage 6 --- Final Validation

``` text
Validate:

- Files detected
- Files processed
- Missing files
- Objectives mapped
- Methodology conflicts
- Unsupported assumptions

Final:
Did all files get processed? YES / NO
```
