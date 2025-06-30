import pandas as pd
import re

INPUT_FILE = "your_file.txt"

# Fixed-width positions (based on your mainframe dump)
colspecs = [
    (0, 6),      # Payment Document
    (7, 15),     # Sequence Num
    (16, 26),    # Payment Date
    (27, 67),    # Payee
    (68, 76),    # Site
    (77, 91),    # Payment Amount
    (92, 102),   # Cleared Date
    (103, 117),  # Cleared Amount
    (118, None)  # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status", "Site Full"
]

def is_header_or_page(line):
    return any(kw in line for kw in [
        "Payment Document", "Payment Register", "BANK:", "Page:", "HARRIS SOB"
    ])

def is_new_record(line):
    return bool(re.match(r'^\s*\d{4}\s+\d{7}', line.strip()))

parsed_rows = []

with open(INPUT_FILE, "r") as f:
    current_record = None
    payee_overflow_lines = []
    
    for line in f:
        line = line.rstrip("\n")
        if not line.strip() or is_header_or_page(line):
            continue

        if is_new_record(line):
            # Process previous record
            if current_record:
                fields = [current_record[start:end].strip() if end else current_record[start:].strip() 
                          for (start, end) in colspecs]

                full_payee = [fields[3]] + [l.strip() for l in payee_overflow_lines[:-1]]
                fields[3] = " ".join(full_payee)
                site_full = payee_overflow_lines[-1].strip() if payee_overflow_lines else ""

                try:
                    fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
                except:
                    fields[5] = None

                try:
                    fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
                except:
                    fields[7] = None

                fields.append(site_full)
                parsed_rows.append(fields)

            # Start new record
            current_record = line
            payee_overflow_lines = []
        else:
            payee_overflow_lines.append(line)

    # Handle final record
    if current_record:
        fields = [current_record[start:end].strip() if end else current_record[start:].strip() 
                  for (start, end) in colspecs]

        full_payee = [fields[3]] + [l.strip() for l in payee_overflow_lines[:-1]]
        fields[3] = " ".join(full_payee)
        site_full = payee_overflow_lines[-1].strip() if payee_overflow_lines else ""

        try:
            fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
        except:
            fields[5] = None

        try:
            fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
        except:
            fields[7] = None

        fields.append(site_full)
        parsed_rows.append(fields)

# Output to DataFrame
df = pd.DataFrame(parsed_rows, columns=columns)
print(df.head())
# Optional: df.to_csv("mainframe_parsed.csv", index=False)