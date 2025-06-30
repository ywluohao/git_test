import re
import pandas as pd

# Input file
INPUT_FILE = "your_file.txt"

# Prepare output
parsed_rows = []
current_record = []

# Precompiled regex
record_start_re = re.compile(r'^\s*\d{4}\s+\d{7}')
main_line_re = re.compile(
    r'^\s*(\d{4})\s+(\d{7})\s+@?(\d{2}-[A-Z]{3}-\d{2})\s+(.+?)\s+([A-Z0-9\-]{3,})\s+([\d,]+\.\d{2})\s+(\d{2}-[A-Z]{3}-\d{2})?\s+([\d,]*\.?\d*)?\s+(\w+)'
)

with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.rstrip()
        if not line.strip():
            continue

        if record_start_re.match(line):
            if current_record:
                # Parse the previous record before starting a new one
                header = current_record[0]
                site_full = current_record[-1]
                payee_overflow = current_record[1] if len(current_record) == 3 else ""
                
                m = main_line_re.match(header)
                if m:
                    fields = list(m.groups())
                    if payee_overflow:
                        fields[3] = fields[3].strip() + " " + payee_overflow.strip()
                    fields.append(site_full.strip())
                    parsed_rows.append(fields)
                else:
                    print("⚠️ Failed to parse record:", header)

            # Start a new record
            current_record = [line]
        else:
            current_record.append(line)

# Don't forget the final record
if current_record:
    header = current_record[0]
    site_full = current_record[-1]
    payee_overflow = current_record[1] if len(current_record) == 3 else ""
    
    m = main_line_re.match(header)
    if m:
        fields = list(m.groups())
        if payee_overflow:
            fields[3] = fields[3].strip() + " " + payee_overflow.strip()
        fields.append(site_full.strip())
        parsed_rows.append(fields)
    else:
        print("⚠️ Failed to parse record:", header)

# Build DataFrame
columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status",
    "Site Full"
]

df = pd.DataFrame(parsed_rows, columns=columns)

# Clean numeric fields
df["Payment Amount"] = df["Payment Amount"].str.replace(",", "").astype(float)
df["Cleared Amount"] = pd.to_numeric(df["Cleared Amount"].str.replace(",", ""), errors="coerce")

# Done
print(df.head())
# df.to_csv("parsed_register.csv", index=False)