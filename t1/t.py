import pandas as pd
import re

# === CONFIG ===
INPUT_FILE = "BMO BANK N.A payment register 11-01-24 thru 04-25-25.txt"

colspecs = [
    (0, 19),     # Payment Document
    (19, 30),    # Sequence Num
    (30, 40),    # Payment Date
    (40, 59),    # Payee (main chunk)
    (59, 68),    # Site
    (68, 100),   # Payment Amount
    (100, 110),  # Cleared Date
    (110, 119),  # Cleared Amount
    (119, None)  # Status
]

columns = [
    "Payment Document", "Sequence Num", "Payment Date", "Payee",
    "Site", "Payment Amount", "Cleared Date", "Cleared Amount", "Status",
    "Site Full", "Page Number", "Page Payment Document"
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

# === MAIN PARSE ===
parsed_rows = []
page_number = None
page_payment_doc = None
current_record = None
payee_lines = []

with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.rstrip("\n")

        if not line.strip():
            continue

        if line.strip().startswith("Page:"):
            m = re.search(r'Page:\s*(\d+)', line)
            if m:
                page_number = int(m.group(1))
            continue

        if "Payment Document:" in line:
            m = re.search(r'Payment Document:\s*(.+)', line)
            if m:
                page_payment_doc = m.group(1).strip()
            continue

        if is_header_or_page(line):
            continue

        if is_new_record(line):
            if current_record:
                # Process previous
                fields = [current_record[start:end].strip() if end else current_record[start:].strip()
                          for (start, end) in colspecs]

                full_payee = [fields[3]] + [l.strip() for l in payee_lines[:-1]]
                fields[3] = " ".join(full_payee)
                site_full = ""

                if payee_lines:
                    last_line = payee_lines[-1].strip()
                    if fields[4].upper() != "OFFICE" and re.search(r'\d{5}|United States|Canada', last_line, re.IGNORECASE):
                        site_full = last_line
                    else:
                        fields[3] += " " + last_line

                try:
                    fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
                except:
                    fields[5] = None

                try:
                    fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
                except:
                    fields[7] = None

                fields += [site_full, page_number, page_payment_doc]
                parsed_rows.append(fields)

            current_record = line
            payee_lines = []
        else:
            payee_lines.append(line)

# Handle last record
if current_record:
    fields = [current_record[start:end].strip() if end else current_record[start:].strip()
              for (start, end) in colspecs]

    full_payee = [fields[3]] + [l.strip() for l in payee_lines[:-1]]
    fields[3] = " ".join(full_payee)
    site_full = ""

    if payee_lines:
        last_line = payee_lines[-1].strip()
        if fields[4].upper() != "OFFICE" and re.search(r'\d{5}|United States|Canada', last_line, re.IGNORECASE):
            site_full = last_line
        else:
            fields[3] += " " + last_line

    try:
        fields[5] = float(fields[5].replace(",", "")) if fields[5] else None
    except:
        fields[5] = None

    try:
        fields[7] = float(fields[7].replace(",", "")) if fields[7] else None
    except:
        fields[7] = None

    fields += [site_full, page_number, page_payment_doc]
    parsed_rows.append(fields)

# === OUTPUT ===
df = pd.DataFrame(parsed_rows, columns=columns)
print(df.head())

# Save to CSV
# df.to_csv("mainframe_parsed_final.csv", index=False)