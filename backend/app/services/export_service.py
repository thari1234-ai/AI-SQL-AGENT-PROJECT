import csv
import io
from typing import Any

from openpyxl import Workbook


def export_csv(columns: list[str], rows: list[dict[str, Any]]) -> bytes:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def export_xlsx(columns: list[str], rows: list[dict[str, Any]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(columns)
    for row in rows:
        sheet.append([row.get(col) for col in columns])

    buffer = io.BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
