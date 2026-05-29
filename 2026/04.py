from pathlib import Path
import json
import re
import time

import pandas as pd
from tqdm import tqdm
from langchain_aws import ChatBedrockConverse


INPUT_FILE = Path("output/results/accountability_evidence.xlsx")
OUTPUT_FILE = Path("output/results/final_audit_accountability_output.xlsx")

MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
REGION = "us-east-1"
SLEEP_SECONDS = 1

llm = ChatBedrockConverse(
    model=MODEL_ID,
    temperature=0,
    region_name=REGION,
)


OBJECTIVE_ORDER = [
    ("Pre-Planning", "Issue letter of engagement"),
    ("Pre-Planning", "Confirm audit resources"),
    ("Pre-Planning", "Engage audit analytics"),

    ("Planning", "Finalize planning memorandum"),
    ("Planning", "Finalize audit scope/program"),
    ("Planning", "Finalize rating areas in MSI"),
    ("Planning", "Prepare/send pull list"),

    ("Fieldwork", "Kickoff meeting"),
    ("Fieldwork", "Execute/document/conclude testing"),
    ("Fieldwork", "Review work papers"),
    ("Fieldwork", "Discuss issues"),
    ("Fieldwork", "Ongoing meetings"),
    ("Fieldwork", "Draft issues"),

    ("Reporting", "Draft report"),
    ("Reporting", "Closing meeting"),
    ("Reporting", "Publish report"),
    ("Reporting", "Close audit"),

    ("Issue Follow Up", "Track issues"),
    ("Issue Follow Up", "Retest issues"),
    ("Issue Follow Up", "Close issues"),
]


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower() for c in df.columns]

    rename_map = {
        "source_file_no": "file_no",
        "source_file_name": "file_name",
        "audit stage": "audit_stage",
        "does what": "does_what",
        "mapped role": "mapped_role",
        "exact language": "exact_language",
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

    return df[keep_cols].fillna("")


def df_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "No evidence rows found for this objective."
    return df.fillna("").to_markdown(index=False)


def parse_json_response(text: str) -> dict:
    text = str(text).strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        return {
            "objective_summary": {},
            "accountability_matrix": {},
            "gaps_conflicts": [
                {
                    "gap_or_conflict": "JSON parse error",
                    "source_files": "",
                    "notes": text[:2000],
                }
            ],
        }


def ordered_groups(df: pd.DataFrame):
    groups = []
    used_keys = set()

    for audit_stage, objective in OBJECTIVE_ORDER:
        mask = (
            df["audit_stage"].astype(str).str.strip().str.lower().eq(audit_stage.lower())
            & df["objective"].astype(str).str.strip().str.lower().eq(objective.lower())
        )

        group = df[mask].copy()
        group["objective_source"] = "Original objective list"

        groups.append(
            (audit_stage, objective, group, "Original objective list")
        )

        used_keys.add((audit_stage.lower(), objective.lower()))

    for (audit_stage, objective), group in df.groupby(["audit_stage", "objective"], dropna=False):
        audit_stage_str = str(audit_stage).strip()
        objective_str = str(objective).strip()
        key = (audit_stage_str.lower(), objective_str.lower())

        if key not in used_keys:
            group = group.copy()
            group["objective_source"] = "Additional objective from source"

            groups.append(
                (
                    audit_stage_str,
                    objective_str,
                    group,
                    "Additional objective from source",
                )
            )

    return groups


def build_objective_prompt(
    audit_stage: str,
    objective: str,
    objective_source: str,
    group: pd.DataFrame,
) -> str:
    raw_table = df_to_markdown(group)

    return f"""
You are creating an objective-level audit accountability result.

Use ONLY the raw evidence table below.

Do not use original files.
Do not use external knowledge.
Do not infer beyond evidence.

Audit Stage: {audit_stage}
Objective: {objective}
Objective Source: {objective_source}

Return valid JSON only.

Required JSON structure:

{{
  "objective_summary": {{
    "audit_stage": "{audit_stage}",
    "objective": "{objective}",
    "objective_source": "{objective_source}",
    "am_evidence": "",
    "sam_evidence": "",
    "director_evidence": "",
    "other_unclear_evidence": "",
    "source_files": "",
    "final_confidence": "",
    "notes": ""
  }},
  "accountability_matrix": {{
    "audit_stage": "{audit_stage}",
    "objective": "{objective}",
    "objective_source": "{objective_source}",
    "am": "",
    "sam": "",
    "director": "",
    "other_unclear": "",
    "approval_required": "",
    "evidence_sources": "",
    "status": ""
  }},
  "gaps_conflicts": [
    {{
      "audit_stage": "{audit_stage}",
      "objective": "{objective}",
      "objective_source": "{objective_source}",
      "gap_or_conflict": "",
      "source_files": "",
      "notes": ""
    }}
  ]
}}

Rules:
- mapped_role = AM goes to AM evidence.
- mapped_role = SAM goes to SAM evidence.
- mapped_role = Director goes to Director evidence.
- mapped_role = Other or Unclear goes to Other / Unclear evidence.
- Preserve file_no, file_name, exact_language, and location in evidence references.
- If approval is explicitly stated, identify it.
- If role is only involved but not accountable, say "Involvement only".
- If evidence conflicts, mark "Conflict detected".
- If there is no evidence for this objective, mark status as "Globally not found".
- If Objective Source is "Additional objective from source", preserve it as an additional source objective.

Raw evidence table:

{raw_table}
"""


def summarize_objectives(df: pd.DataFrame):
    objective_summary_rows = []
    accountability_rows = []
    gaps_rows = []

    groups = ordered_groups(df)

    for audit_stage, objective, group, objective_source in tqdm(
        groups,
        desc="Processing objectives",
        unit="objective",
    ):
        prompt = build_objective_prompt(
            audit_stage=audit_stage,
            objective=objective,
            objective_source=objective_source,
            group=group,
        )

        try:
            result = llm.invoke(prompt)
            parsed = parse_json_response(result.content)
        except Exception as e:
            parsed = {
                "objective_summary": {
                    "audit_stage": audit_stage,
                    "objective": objective,
                    "objective_source": objective_source,
                    "am_evidence": "",
                    "sam_evidence": "",
                    "director_evidence": "",
                    "other_unclear_evidence": "",
                    "source_files": "",
                    "final_confidence": "Error",
                    "notes": str(e),
                },
                "accountability_matrix": {
                    "audit_stage": audit_stage,
                    "objective": objective,
                    "objective_source": objective_source,
                    "am": "",
                    "sam": "",
                    "director": "",
                    "other_unclear": "",
                    "approval_required": "",
                    "evidence_sources": "",
                    "status": "Error",
                },
                "gaps_conflicts": [
                    {
                        "audit_stage": audit_stage,
                        "objective": objective,
                        "objective_source": objective_source,
                        "gap_or_conflict": "LLM call failed",
                        "source_files": "",
                        "notes": str(e),
                    }
                ],
            }

        obj_summary = parsed.get("objective_summary", {}) or {}
        acct = parsed.get("accountability_matrix", {}) or {}
        gaps = parsed.get("gaps_conflicts", []) or []

        obj_summary.setdefault("audit_stage", audit_stage)
        obj_summary.setdefault("objective", objective)
        obj_summary.setdefault("objective_source", objective_source)

        acct.setdefault("audit_stage", audit_stage)
        acct.setdefault("objective", objective)
        acct.setdefault("objective_source", objective_source)

        objective_summary_rows.append(obj_summary)
        accountability_rows.append(acct)

        for gap in gaps:
            gap.setdefault("audit_stage", audit_stage)
            gap.setdefault("objective", objective)
            gap.setdefault("objective_source", objective_source)
            gaps_rows.append(gap)

        time.sleep(SLEEP_SECONDS)

    return (
        pd.DataFrame(objective_summary_rows),
        pd.DataFrame(accountability_rows),
        pd.DataFrame(gaps_rows),
    )


def build_objective_to_document_matrix(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for audit_stage, objective, group, objective_source in ordered_groups(df):
        if group.empty:
            source_files = []
        else:
            source_files = (
                group[["file_no", "file_name"]]
                .drop_duplicates()
                .apply(lambda r: f"{r['file_no']} - {r['file_name']}", axis=1)
                .tolist()
            )

        rows.append({
            "audit_stage": audit_stage,
            "objective": objective,
            "objective_source": objective_source,
            "supporting_files": "; ".join(source_files),
            "reference_count": len(group),
        })

    return pd.DataFrame(rows)


def build_validation_summary(
    df: pd.DataFrame,
    accountability_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for audit_stage, objective, group, objective_source in ordered_groups(df):
        if group.empty:
            source_files = []
        else:
            source_files = (
                group[["file_no", "file_name"]]
                .drop_duplicates()
                .apply(lambda r: f"{r['file_no']} - {r['file_name']}", axis=1)
                .tolist()
            )

        status_row = accountability_df[
            (accountability_df["audit_stage"].astype(str).str.lower() == audit_stage.lower())
            & (accountability_df["objective"].astype(str).str.lower() == objective.lower())
        ]

        final_status = ""
        if not status_row.empty and "status" in status_row.columns:
            final_status = str(status_row.iloc[0].get("status", ""))

        rows.append({
            "audit_stage": audit_stage,
            "objective": objective,
            "objective_source": objective_source,
            "evidence_found": "YES" if len(group) > 0 else "NO",
            "source_files": "; ".join(source_files),
            "evidence_rows": len(group),
            "final_status": final_status,
        })

    return pd.DataFrame(rows)


def save_to_excel(
    raw_df: pd.DataFrame,
    objective_doc_df: pd.DataFrame,
    objective_summary_df: pd.DataFrame,
    accountability_df: pd.DataFrame,
    gaps_df: pd.DataFrame,
    validation_df: pd.DataFrame,
):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        raw_df.to_excel(writer, sheet_name="Combined Raw Evidence", index=False)
        objective_doc_df.to_excel(writer, sheet_name="Objective Document Matrix", index=False)
        objective_summary_df.to_excel(writer, sheet_name="Aggregated Objective View", index=False)
        accountability_df.to_excel(writer, sheet_name="Accountability Matrix", index=False)
        gaps_df.to_excel(writer, sheet_name="Gaps Conflicts", index=False)
        validation_df.to_excel(writer, sheet_name="Validation Summary", index=False)

        for sheet_name, worksheet in writer.sheets.items():
            worksheet.freeze_panes(1, 0)
            worksheet.autofilter(0, 0, 0, 20)
            worksheet.set_column(0, 0, 22)
            worksheet.set_column(1, 1, 38)
            worksheet.set_column(2, 20, 45)

    print(f"Saved final Excel output to: {OUTPUT_FILE}")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)
    df = normalize_columns(df)

    print(f"Rows loaded: {len(df)}")
    print(f"Objectives found in evidence: {df['objective'].nunique()}")

    objective_doc_df = build_objective_to_document_matrix(df)

    objective_summary_df, accountability_df, gaps_df = summarize_objectives(df)

    validation_df = build_validation_summary(df, accountability_df)

    save_to_excel(
        raw_df=df,
        objective_doc_df=objective_doc_df,
        objective_summary_df=objective_summary_df,
        accountability_df=accountability_df,
        gaps_df=gaps_df,
        validation_df=validation_df,
    )


if __name__ == "__main__":
    main()