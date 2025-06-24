import pdfplumber
import pandas as pd

pdf_path = "your_file.pdf"
all_rows = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.find_tables()
        for table in tables:
            data = table.extract()
            if not data:
                continue

            headers = data[0]
            for row in data[1:]:
                while len(row) < len(headers):
                    row.append('')  # Fill blank cells
                row_dict = dict(zip(headers, row))
                all_rows.append(row_dict)

df = pd.DataFrame(all_rows)
print(df.head())