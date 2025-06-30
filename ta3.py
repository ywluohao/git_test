import pandas as pd
import re

# --- CONFIG ---
INPUT_FILE = "your_file.txt"  # ← Replace with your actual input file

# Hardcoded fixed-width field positions (based on your screenshot)
colspecs = [
    (0, 6),      # Payment Document
    (7, 15),     # Sequence Num
    (16, 26),    # Payment Date
    (27, 67),    # Payee (main part, may overflow)
    (68, 76),    # Site
    (77, 91),    # Payment Amount
    (92, 102),   # Cleared Date
    (103, 117),  # Cleared Amount
    (118, None)  # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status"
]

# Helper to detect start of a record
def is_new_record(line):
    return bool(re.match(r'^\s*\d{4}\s+\d{7}', line.strip()))

# Skip junk like headers on each page
def is_header_or_page_line(line):
    return any([
        line.startswith("Payment Document"),
        "Payment Register" in line,
        "BANK:" in line,
        line.strip().startswith("Page:"),
        line.strip().startswith("HARRIS SOB")
    ])

# --- STEP 1: Read and chunk lines into full records ---
with open(INPUT_FILE, "r") as f:
    lines = [line.rstrip("\n") for line in f if line.strip()]

records = []
current_record = []

for line in lines:
    if is_header_or_page_line(line):
        continue
    if is_new_record(line):
        if current_record:
            records.append(current_record)
        current_record = [line]
    else:
        current_record.append(line)

# Add last record
if current_record:
    records.append(current_record)

# --- STEP 2: Parse records ---
parsed_rows = []

for rec in records:
    if len(rec) < 2:
        continue  # skip junk

    header = rec[0]
    site_full = rec[-1]
    payee_overflow_lines = rec[1:-1]  # All lines between header and site = extra payee

    # Parse fields from fixed-width header line
    fields = [header[start:end].strip() if end else header[start:].strip() for (start, end) in colspecs]

    # Combine multiline payee
    full_payee = [fields[3]] + [line.strip() for line in payee_overflow_lines]
    fields[3] = " ".join(full_payee)

    # Clean numeric fields
    try:
        fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
    except:
        fields[5] = None

    try:
        fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
    except:
        fields[7] = None

    # Add site full as last column
    fields.append(site_full.strip())
    parsed_rows.append(fields)

# --- STEP 3: Output to DataFrame ---
df = pd.DataFrame(parsed_rows, columns=columns + ["Site Full"])

# --- DONE ---
print(df.head())
# Optionally save to file:
# df.to_csv("parsed_mainframe_output.csv", index=False)