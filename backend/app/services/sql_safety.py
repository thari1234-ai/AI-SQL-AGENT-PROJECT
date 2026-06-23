import re

FORBIDDEN = ["drop", "delete", "update", "alter", "truncate", "create", "insert", "grant", "revoke"]


def validate_readonly_sql(sql: str) -> str:
    cleaned = sql.strip().rstrip(";")
    lowered = cleaned.lower()

    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    for keyword in FORBIDDEN:
        if re.search(rf"\b{keyword}\b", lowered):
            raise ValueError(f"Query blocked due to forbidden keyword: {keyword.upper()}")

    if ";" in cleaned:
        raise ValueError("Multiple statements are not allowed")

    return cleaned
