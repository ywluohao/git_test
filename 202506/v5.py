import pdfplumber
import pandas as pd
import re

rows = []

with pdfplumber.open("your_file.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text(layout=True)
        lines = text.split('\n')

        collecting = False  # Flag to start collecting rows *after* header

        for line in lines:
            stripped = line.strip()

            # Use the line with dashes as the divider between header and table
            if re.match(r'^[-\s]{10,}$', stripped):
                collecting = True
                continue

            if not collecting:
                continue

            if not stripped:
                continue

            # Split using 2+ spaces, preserve empty columns
            cols = re.split(r'\s{2,}', stripped)

            # Optional: filter junk rows (e.g., totals, footers)
            if len(cols) < 5:
                continue

            rows.append(cols)

# Normalize to match longest row
max_len = max(len(r) for r in rows)
cleaned_rows = [r + [''] * (max_len - len(r)) for r in rows]

df = pd.DataFrame(cleaned_rows)
df.columns = [
    "Transaction Ref", "Related Ref", "Beneficiary", "Entry Date",
    "Value Date", "Debits", "Credits", "Balance"
][:max_len]  # truncate column names if needed

print(df.head(10))