import pandas as pd
import re

# Read raw lines
with open("your_file.txt", "r") as file:
    lines = file.readlines()

# Step 1: Extract only data lines (skip headers and footers)
data_lines = []
current_record = ""

for line in lines:
    # Detect start of a new record (payment # is 4 digits)
    if re.match(r'^\s*\d{4}\s+\d{7}', line):
        if current_record:
            data_lines.append(current_record)
        current_record = line.rstrip()
    elif line.strip() == "":
        continue
    else:
        # Continuation line — append with space
        current_record += " " + line.strip()

# Add last record
if current_record:
    data_lines.append(current_record)

# Write preprocessed output to temp file
with open("cleaned_register.txt", "w") as f:
    for rec in data_lines:
        f.write(rec + "\n")

# Step 2: Use fixed-width parsing
colspecs = [
    (0, 6),     # Payment Document
    (7, 14),    # Sequence Num
    (15, 25),   # Date
    (26, 60),   # Payee
    (61, 68),   # Site
    (69, 82),   # Amount
    (83, 94),   # Date
    (95, 108),  # Cleared Amount
    (109, None) # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status"
]

df = pd.read_fwf("cleaned_register.txt", colspecs=colspecs, names=columns)

# Optional: clean up
df["Payment Amount"] = pd.to_numeric(df["Payment Amount"].str.replace(",", ""), errors="coerce")
df["Cleared Amount"] = pd.to_numeric(df["Cleared Amount"].str.replace(",", ""), errors="coerce")

print(df.head())