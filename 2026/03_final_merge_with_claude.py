from pathlib import Path
import re
import time
import pandas as pd
from tqdm import tqdm
from langchain_aws import ChatBedrockConverse


INPUT_FILE = Path("output/results/accountability_evidence.xlsx")
OUTPUT_DIR = Path("output/results/objective_summaries")
FINAL_OUTPUT = Path("output/results/final_objective_merge.md")

MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
REGION = "us-east-1"

SLEEP_SECONDS = 1

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


llm = ChatBedrockConverse(
    model=MODEL_ID,
    temperature=0,
    region_name=REGION,
)


def safe_filename(value: str) -> str:
    value = str(value)
    value = re.sub(r"[^\w\-]+", "_", value)
    return value.strip("_")[:120]


def df_to_markdown(df: pd.DataFrame) -> str:
    df = df.fillna("")
    return df.to_markdown(index=False)


def build_objective_prompt(audit_stage: str, objective: str, df: pd.DataFrame) -> str:
    raw_table = df_to_markdown(df)

    return f"""
You are creating an objective-level audit accountability summary.

Use ONLY the raw evidence table below.

Do not use original files.
Do not use external knowledge.
Do not infer beyond evidence.
Do not summarize away evidence.

Audit Stage: {audit_stage}
Objective: {objective}

For this objective only, produce:

## Objective Summary

| Audit Stage | Objective | AM Evidence | SAM Evidence | Director Evidence | Other / Unclear Evidence | Source Files | Final Confidence | Notes |
|---|---|---|---|---|---|---|---|---|

## Accountability Matrix Row

| Audit Stage | Objective | AM | SAM | Director | Other / Unclear | Approval Required | Evidence Sources | Status |
|---|---|---|---|---|---|---|---|---|

## Gaps / Conflicts

| Audit Stage | Objective | Gap or Conflict | Source Files | Notes |
|---|---|---|---|---|

Rules:
- mapped_role = AM goes to AM Evidence.
- mapped_role = SAM goes to SAM Evidence.
- mapped_role = Director goes to Director Evidence.
- mapped_role = Other or Unclear goes to Other / Unclear Evidence.
- Preserve file_no, file_name, exact_language, and location.
- If approval is stated, identify it.
- If role is only involved but not accountable, say "Involvement only".
- If evidence conflicts, mark "Conflict detected".

Raw evidence table:

{raw_table}
"""


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


def summarize_each_objective(df: pd.DataFrame) -> list[Path]:
    summary_paths = []

    grouped = list(df.groupby(["audit_stage", "objective"], dropna=False))

    for idx, ((audit_stage, objective), group) in enumerate(
        tqdm(grouped, desc="Summarizing objectives", unit="objective"),
        start=1,
    ):
        audit_stage = str(audit_stage)
        objective = str(objective)

        filename = f"{idx:02d}_{safe_filename(audit_stage)}__{safe_filename(objective)}.md"
        output_path = OUTPUT_DIR / filename

        if output_path.exists():
            summary_paths.append(output_path)
            continue

        prompt = build_objective_prompt(audit_stage, objective, group)

        try:
            result = llm.invoke(prompt)
            output_path.write_text(result.content, encoding="utf-8")
            summary_paths.append(output_path)
        except Exception as e:
            error_text = f"# ERROR\n\nAudit Stage: {audit_stage}\n\nObjective: {objective}\n\nError:\n\n{e}\n"
            output_path.write_text(error_text, encoding="utf-8")
            summary_paths.append(output_path)

        time.sleep(SLEEP_SECONDS)

    return summary_paths


def build_final_merge_prompt(summary_text: str) -> str:
    return f"""
You are creating the final audit accountability output.

Use ONLY the objective summaries below.

Do not use original files.
Do not use external knowledge.

Create:

# Final Audit Accountability Output

## 1. Final Aggregated Objective View

| Audit Stage | Objective | AM Evidence | SAM Evidence | Director Evidence | Other Evidence | Source Files | Final Confidence | Notes |
|---|---|---|---|---|---|---|---|---|

## 2. Final Accountability Matrix

| Audit Stage | Objective | AM | SAM | Director | Other / Unclear | Approval Required | Evidence Sources | Status |
|---|---|---|---|---|---|---|---|---|

## 3. Cross-Objective Gaps and Conflicts

| Audit Stage | Objective | Gap or Conflict | Source Files | Notes |
|---|---|---|---|---|

## 4. Final Validation Summary

| Audit Stage | Objective | Evidence Found YES/NO | Source Files | Final Status |
|---|---|---|---|---|

Final summary:
- Objectives processed:
- Objectives with evidence:
- Objectives globally not found:
- Conflicts detected:
- Final status YES/NO:

Objective summaries:

{summary_text}
"""


def merge_objective_summaries(summary_paths: list[Path]) -> None:
    parts = []
    for path in summary_paths:
        parts.append(f"\n\n<!-- {path.name} -->\n")
        parts.append(path.read_text(encoding="utf-8"))

    combined = "\n".join(parts)

    prompt = build_final_merge_prompt(combined)

    print("Sending final merge of objective summaries to Claude...")
    result = llm.invoke(prompt)

    FINAL_OUTPUT.write_text(result.content, encoding="utf-8")
    print(f"Saved final output to: {FINAL_OUTPUT}")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)
    df = normalize_columns(df)

    print(f"Rows loaded: {len(df)}")
    print(f"Objectives: {df['objective'].nunique()}")

    summary_paths = summarize_each_objective(df)

    print(f"Objective summaries saved to: {OUTPUT_DIR}")

    merge_objective_summaries(summary_paths)


if __name__ == "__main__":
    main()