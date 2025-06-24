import pdfplumber
import pandas as pd

pdf_path = "sample.pdf"  # Use the real PDF here

dfs = []
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        # Skip cover pages or non-table pages
        if i >= 10:  # You showed pages 11–14
            table = page.extract_table({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 5,
                "snap_tolerance": 3,
                "edge_min_length": 3
            })
            if table:
                df = pd.DataFrame(table)
                dfs.append(df)

# Combine and clean
df_all = pd.concat(dfs, ignore_index=True)

# Optional: use first non-empty row as header
header_row = df_all[df_all.notna().sum(axis=1) > 3].iloc[0]
df_all.columns = header_row
df_all = df_all[df_all.index > header_row.name].reset_index(drop=True)

# Convert blank cells to NaN explicitly (optional)
df_all = df_all.replace("", pd.NA)

print(df_all.head())