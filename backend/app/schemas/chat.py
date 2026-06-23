from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=2)
    conversation_id: str | None = None


class ChartSpec(BaseModel):
    type: str
    x_key: str | None = None
    y_key: str | None = None
    category_key: str | None = None
    value_key: str | None = None


class ChatResponse(BaseModel):
    prompt: str
    sql: str
    explanation: str
    insight_summary: str
    key_observations: list[str]
    recommendations: list[str]
    rows: list[dict[str, Any]]
    columns: list[str]
    chart: ChartSpec
    execution_ms: float
    timestamp: datetime
