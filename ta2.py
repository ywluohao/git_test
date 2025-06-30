import pandas as pd
import re

INPUT_FILE = "your_file.txt"

# Hardcoded fixed-width layout
colspecs = [
    (0, 18),     # Payment Document
    (18, 33),    # Sequence Num
    (33, 44),    # Payment Date
    (44, 76),    # Payee (main chunk)
    (76, 85),    # Site
    (85, 101),   # Payment Amount
    (101, 113),  # Cleared Date
    (113, 130),  # Cleared Amount
    (130, None)  # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status"
]

def is_record_start(line):
    return bool(re.match(r'^\s*\d{4,}', line.strip()[:6]))

parsed_rows = []
with open(INPUT_FILE, "r") as f:
    lines = [line.rstrip('\n') for line in f if line.strip()]

i = 0
while i < len(lines):
    line = lines[i]

    # Skip page headers
    if any([
        line.startswith("Payment Document"),
        "Payment Register" in line,
        "BANK:" in line,
        line.strip().startswith("Page:"),
        line.strip().startswith("HARRIS SOB")
    ]):
        i += 1
        continue

    if not is_record_start(line):
        i += 1
        continue

    # Start new record
    main_line = line
    payee_lines = []
    i += 1

    # Collect all payee overflow lines until we hit Site Full
    while i < len(lines) and not is_record_start(lines[i]):
        payee_lines.append(lines[i])
        i += 1

    # Site Full is always the last of the payee_lines
    site_full = payee_lines.pop() if payee_lines else ""

    # Parse fixed-width fields from the main line
    fields = [main_line[start:end].strip() if end else main_line[start:].strip() for (start, end) in colspecs]

    # Combine payee overflow into main payee
    if payee_lines:
        fields[3] += " " + " ".join(line.strip() for line in payee_lines)

    # Clean numeric fields
    try:
        fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
    except:
        fields[5] = None

    try:
        fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
    except:
        fields[7] = None

    # Append site full
    fields.append(site_full.strip())
    parsed_rows.append(fields)

# Build DataFrame
df = pd.DataFrame(parsed_rows, columns=columns + ["Site Full"])
print(df.head())
# df.to_csv("parsed_mainframe_output.csv", index=False)