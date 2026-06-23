import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings


def execute_sql(db: Session, sql: str) -> tuple[list[dict[str, Any]], list[str], float]:
    start = time.perf_counter()
    db.execute(text(f"SET LOCAL statement_timeout = {settings.sql_timeout_seconds * 1000}"))
    result = db.execute(text(sql))
    rows = [dict(row._mapping) for row in result.fetchmany(settings.sql_max_rows)]
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    columns = list(rows[0].keys()) if rows else []
    return rows, columns, elapsed_ms
