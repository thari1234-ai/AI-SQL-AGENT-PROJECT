from collections.abc import Sequence


def detect_chart(columns: list[str], rows: Sequence[dict]) -> dict:
    if not columns or not rows:
        return {"type": "table"}

    sample = rows[0]
    numeric_cols = [k for k, v in sample.items() if isinstance(v, (int, float))]
    non_numeric_cols = [k for k in columns if k not in numeric_cols]

    if len(columns) >= 2 and non_numeric_cols and numeric_cols:
        if any("date" in c.lower() or "month" in c.lower() or "year" in c.lower() for c in columns):
            return {"type": "line", "x_key": non_numeric_cols[0], "y_key": numeric_cols[0]}
        return {"type": "bar", "x_key": non_numeric_cols[0], "y_key": numeric_cols[0]}

    if len(numeric_cols) >= 2:
        return {"type": "scatter", "x_key": numeric_cols[0], "y_key": numeric_cols[1]}

    if len(columns) == 2:
        return {"type": "pie", "category_key": columns[0], "value_key": columns[1]}

    return {"type": "table"}
