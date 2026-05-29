from pathlib import Path
import pandas as pd
from langchain_aws import ChatBedrockConverse

INPUT_FILE = Path("output/results/accountability_evidence.xlsx")
OUTPUT_MD = Path("output/results/final_audit_accountability_output.md")

MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
REGION = "us-east-1"

llm = ChatBedrockConverse(
    model=MODEL_ID,
    temperature=0,
    region_name=REGION,
)

FINAL_MERGE_PROMPT = """
You are creating the final audit accountability output.

Use ONLY the uploaded raw evidence table below.

Do not use original source files.
Do not use external knowledge.
Do not infer accountability beyond evidence.

Each row is one document-level raw evidence item.

Column meaning:
- file_no = source file number
- file_name = source document
- audit_stage = audit stage
- objective = audit objective
- who = source role/person/team
- does_what = activity/event
- mapped_role = AM, SAM, Director, Other, or Unclear
- exact_language = source wording
- location = page/section/table/sheet location
- notes = extraction notes

For final aggregation:
- mapped_role = AM goes to AM Evidence
- mapped_role = SAM goes to SAM Evidence
- mapped_role = Director goes to Director Evidence
- mapped_role = Other or Unclear goes to Other Evidence

Preserve:
- file_no
- file_name
- exact_language
- location

Required output:

# Final Audit Accountability Output

## 1. Combined Document-Level Raw Data

| File No | File Name | Audit Stage | Objective | Activity/Event | Role | Exact Language | Page/Location | Notes |
|---|---|---|---|---|---|---|---|---|

## 2. Final Aggregated Objective View

| Audit Stage | Objective | AM Evidence | SAM Evidence | Director Evidence | Other Evidence | Source Files | Final Confidence | Notes |
|---|---|---|---|---|---|---|---|---|

Confidence rules:
- High: explicit ownership, responsibility, review, approval, or required action is stated
- Medium: role involvement is stated but ownership is not fully explicit
- Low: exact wording appears relevant but role/accountability is unclear
- Conflict detected: evidence conflicts
- Globally not found: no evidence found

## 3. Final Accountability Matrix

| Audit Stage | Objective | AM | SAM | Director | Approval Required | Evidence Sources | Final Confidence | Status |
|---|---|---|---|---|---|---|---|---|

Status values:
- Confirmed
- Involvement only
- Recommended assumption
- Conflict detected
- Globally not found

## 4. Final Swimlane

Group by:
- Pre-Planning
- Planning
- Fieldwork
- Reporting
- Issue Follow Up

For each stage, show:
### AM
### SAM
### Director
### Other / Unclear

Include source references.

## 5. Cross-Batch Gaps and Conflicts

| Audit Stage | Objective | Gap or Conflict | Source Files | Notes |
|---|---|---|---|---|

## 6. Final Validation Summary

| Audit Stage | Objective | Evidence Found YES/NO | Source Files | Final Status |
|---|---|---|---|---|

Final summary:
- Total raw evidence rows:
- Objectives with evidence:
- Objectives globally not found:
- Conflicts detected:
- Final status YES/NO:
"""


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    df = df.fillna("")
    return df.to_markdown(index=False)


def build_prompt(df: pd.DataFrame) -> str:
    raw_table = dataframe_to_markdown(df)

    return f"""
{FINAL_MERGE_PROMPT}

Raw evidence table:

{raw_table}
"""


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)

    # Normalize expected columns
    df.columns = [c.strip().lower() for c in df.columns]

    rename_map = {
        "source_file_no": "file_no",
        "source_file_name": "file_name",
        "audit stage": "audit_stage",
        "audit_stage": "audit_stage",
        "objective": "objective",
        "who": "who",
        "does what": "does_what",
        "does_what": "does_what",
        "mapped role": "mapped_role",
        "mapped_role": "mapped_role",
        "exact language": "exact_language",
        "exact_language": "exact_language",
        "location": "location",
        "notes": "notes",
    }

    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})

    keep_cols = [
        "file_no",
        "file_name",
        "audit_stage",
        "objective",
        "who",
        "does_what",
        "mapped_role",
        "exact_language",
        "location",
        "notes",
    ]

    for col in keep_cols:
        if col not in df.columns:
            df[col] = ""

    df = df[keep_cols]

    prompt = build_prompt(df)

    print("Sending final merge request to Claude...")
    result = llm.invoke(prompt)

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(result.content, encoding="utf-8")

    print(f"Saved final output to: {OUTPUT_MD}")


if __name__ == "__main__":
    main()