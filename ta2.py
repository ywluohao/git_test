import re
import pandas as pd

with open("your_file.txt", "r") as f:
    lines = [line.rstrip() for line in f if line.strip()]

records = []
i = 0
while i < len(lines):
    line = lines[i]

    if re.match(r'^\s*\d{4}\s+\d{7}', line):
        payment_line = line
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        has_extra_line = (
            not re.match(r'^\s*\d{4}\s+\d{7}', next_line)
            and not next_line.startswith("HARRIS SOB")
            and "BANK" not in next_line
        )

        if has_extra_line:
            site_extra = next_line.strip()
            i += 1
        else:
            site_extra = ""

        records.append((payment_line, site_extra))

    i += 1