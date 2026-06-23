from datetime import datetime
from typing import Any

from pydantic import BaseModel


class QueryHistoryItem(BaseModel):
    id: int
    prompt: str
    sql_text: str
    explanation: str
    insight_summary: str
    chart_type: str
    execution_ms: float
    row_count: int
    result_json: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
