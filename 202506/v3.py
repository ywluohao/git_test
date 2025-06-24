import pdfplumber
import pandas as pd
from collections import defaultdict

pdf_path = "your_file.pdf"
all_rows = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        words = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=True)

        lines = defaultdict(list)
        for word in words:
            y = round(word['top'], 1)
            lines[y].append((word['x0'], word['text']))

        for y in sorted(lines):
            row = [text for _, text in sorted(lines[y])]
            all_rows.append(row)

# Convert to DataFrame (you can set your own columns)
df = pd.DataFrame(all_rows)
df = df[df[0].str.match(r'^[A-Z0-9]{8,}')]  # filter for transaction rows if needed
df.reset_index(drop=True, inplace=True)
print(df.head())