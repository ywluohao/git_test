def extract_xlsx(path: Path):
    rows = []
    wb = load_workbook(path, data_only=True, read_only=True)

    for ws in wb.worksheets:
        for row_idx, row in enumerate(ws.iter_rows(), start=1):
            values = []
            cell_refs = []

            for cell in row:
                if cell.value is not None:
                    value = str(cell.value).strip()
                    if value:
                        values.append(value)
                        cell_refs.append(cell.coordinate)

            if values:
                rows.append({
                    "file_name": path.name,
                    "file_type": "XLSX",
                    "location": f"Sheet: {ws.title} | Row {row_idx} | Cells: {','.join(cell_refs)}",
                    "text": " | ".join(values),
                })

    return rows