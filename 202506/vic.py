import pdfplumber
import pandas as pd
import re

pdf_path = "your_file.pdf"

account_number = None
all_rows = []
headers_keywords = ['Transaction Reference', 'Value Date', 'Debits', 'Credits', 'Balance']

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        # Try to extract account number
        if not account_number:
            match = re.search(r'Account Number\s+(\d{3}-\d{4}-\d{3})', text)
            if match:
                account_number = match.group(1)

        # Heuristic: Skip pages without table-like keywords
        if not all(keyword in text for keyword in headers_keywords):
            continue  # skip header or non-transaction pages

        # Extract table
        table = page.extract_table()
        if table:
            headers = table[0]
            rows = table[1:]
            for row in rows:
                if any(cell.strip() for cell in row if cell):  # skip empty rows
                    row_dict = dict(zip(headers, row))
                    all_rows.append(row_dict)

# Convert to DataFrame
df = pd.DataFrame(all_rows)

# Add account number column
df['Account Number'] = account_number

# Optional cleanup: Normalize numbers
for col in ['Debits (U.S. Dollars)', 'Credits (U.S. Dollars)', 'Balance (U.S. Dollars)']:
    if col in df.columns:
        df[col] = df[col].str.replace(',', '').astype(float, errors='ignore')

print(df.head())