import re
import pandas as pd

# --- CONFIG ---
INPUT_FILE = "your_file.txt"  # change this to your actual file path

# --- STEP 1: Read and preprocess ---
with open(INPUT_FILE, "r") as f:
    lines = [line.rstrip() for line in f if line.strip()]

records = []
i = 0
while i < len(lines):
    line = lines[i]

    # Detect start of new record
    if re.match(r'^\s*\d{4}\s+\d{7}', line):
        payment_line = line
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        # Determine if there's a continuation line with address
        has_extra_line = (
            not re.match(r'^\s*\d{4}\s+\d{7}', next_line)
            and not next_line.startswith("HARRIS SOB")
            and "BANK" not in next_line
            and "Payment Register" not in next_line
        )

        if has_extra_line:
            site_extra = next_line.strip()
            i += 1  # Skip next line in loop
        else:
            site_extra = ""

        records.append((payment_line, site_extra))
    i += 1

# --- STEP 2: Parse each record ---
parsed = []
for payment_line, site_extra in records:
    match = re.match(
        r'^\s*(\d{4})\s+(\d{7})\s+@?(\d{2}-[A-Z]{3}-\d{2})\s+(.+?)\s+([A-Z0-9\- ]{3,})\s+([\d,]+\.\d{2})\s+(\d{2}-[A-Z]{3}-\d{2})?\s+([\d,]*\.?\d*)?\s+(\w+)',
        payment_line
    )
    if match:
        fields = list(match.groups())
        site_code = fields[4].strip()
        site_full = site_code + " " + site_extra if site_extra else site_code
        fields.append(site_full)
        parsed.append(fields)
    else:
        print("⚠️ Failed to parse:\n", payment_line)

# --- STEP 3: Build dataframe ---
columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status",
    "Site Full"
]

df = pd.DataFrame(parsed, columns=columns)

# --- STEP 4: Clean up numeric fields ---
df["Payment Amount"] = df["Payment Amount"].str.replace(",", "").astype(float)
df["Cleared Amount"] = pd.to_numeric(df["Cleared Amount"].str.replace(",", ""), errors="coerce")

# --- STEP 5: Done! ---
print(df.head())

# Optional: save to CSV
# df.to_csv("parsed_payment_register.csv", index=False)