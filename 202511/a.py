# pip install mammoth beautifulsoup4
import mammoth, json, csv
from bs4 import BeautifulSoup
from pathlib import Path

DOCX = "input.docx"
OUT_HTML = "input.html"
OUT_JSON = "bullets_by_heading.json"
OUT_CSV  = "bullets_by_heading.csv"

# 1) DOCX → HTML
with open(DOCX, "rb") as f:
    html = mammoth.convert_to_html(f).value
Path(OUT_HTML).write_text(html, encoding="utf-8")   # for eyeballing

# 2) Parse headings + bullets
soup = BeautifulSoup(html, "html.parser")

def is_heading(tag):
    return tag.name in {"h1","h2","h3","h4","h5","h6"}

def li_text(li):
    # flatten nested inline tags
    return li.get_text(" ", strip=True)

# group bullets under the most recent heading
sections = []  # [{heading, level, items:[str]}]
current = {"heading":"ROOT","level":0,"items":[]}
sections.append(current)

for el in soup.body.descendants:
    if not getattr(el, "name", None):
        continue
    if is_heading(el):
        current = {"heading": el.get_text(" ", strip=True),
                   "level": int(el.name[1]), "items":[]}
        sections.append(current)
    elif el.name == "li":
        current["items"].append(li_text(el))

# 3) Keep only sections with bullets
sections = [s for s in sections if s["items"]]

# 4) Optional: filter to your three attachment blocks
targets = {
    "Audit Report (See attachments):",
    "Task Details (Letter of Engagement) (See Attachments):",
    "Task Details (Planning Memo) (See Attachments):",
}
filtered = [s for s in sections if s["heading"] in targets] or sections

# 5) Save JSON and CSV
Path(OUT_JSON).write_text(json.dumps(filtered, ensure_ascii=False, indent=2), encoding="utf-8")
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["heading","level","item"])
    for s in filtered:
        for it in s["items"]:
            w.writerow([s["heading"], s["level"], it])

print(f"Wrote {OUT_HTML}, {OUT_JSON}, {OUT_CSV}")