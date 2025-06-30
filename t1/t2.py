import pandas as pd
import re

# --- CONFIG ---
INPUT_FILE = "BMO BANK N.A payment register 11-01-24 thru 04-25-25.txt"

colspecs = [
    (0, 19),     # Payment Document
    (19, 30),    # Sequence Num
    (30, 40),    # Payment Date
    (40, 59),    # Payee (main part)
    (59, 68),    # Site
    (68, 100),   # Payment Amount
    (100, 110),  # Cleared Date
    (110, 119),  # Cleared Amount
    (119, None)  # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status",
    "Site Full"
]

def is_header_or_page(line):
    return any(kw in line for kw in [
        "Payment Type: All",
        "Bank Account Currency: USD ( US Dollar )",
        "BANK: HARRIS BANK",
        "Branch : Expense Accounting",
        "Display Supplier Address: Yes",
        "Page:",
        "Payment Register",
        "HARRIS SOB",
        "**** End of Report ****",
        "-" * 5, "*" * 5, "=" * 5
    ])

def is_new_record(line):
    return bool(re.match(r'^\s*\d{4,}\s+\d{7}', line.strip()))

# --- MAIN PARSE LOOP ---
parsed_rows = []
current_record = None
payee_lines = []

with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.rstrip("\n")

        if not line.strip() or is_header_or_page(line):
            continue

        if is_new_record(line):
            if current_record:
                fields = [current_record[start:end].strip() if end else current_record[start:].strip()
                          for (start, end) in colspecs]

                site_full = ""
                if payee_lines:
                    last_line = payee_lines[-1].strip()
                    if fields[4].upper() == "OFFICE":
                        # No Site Full — all payee lines go into Payee
                        full_payee = [fields[3]] + [l.strip() for l in payee_lines]
                    else:
                        site_full = last_line
                        full_payee = [fields[3]] + [l.strip() for l in payee_lines[:-1]]
                    fields[3] = " ".join(full_payee)

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

            current_record = line
            payee_lines = []
        else:
            payee_lines.append(line)

# Handle last record
if current_record:
    fields = [current_record[start:end].strip() if end else current_record[start:].strip()
              for (start, end) in colspecs]

    site_full = ""
    if payee_lines:
        last_line = payee_lines[-1].strip()
        if fields[4].upper() == "OFFICE":
            full_payee = [fields[3]] + [l.strip() for l in payee_lines]
        else:
            site_full = last_line
            full_payee = [fields[3]] + [l.strip() for l in payee_lines[:-1]]
        fields[3] = " ".join(full_payee)

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

# --- FINAL OUTPUT ---
df = pd.DataFrame(parsed_rows, columns=columns)
print(df.head())

# Optional: save to file
# df.to_csv("mainframe_parsed_final.csv", index=False)