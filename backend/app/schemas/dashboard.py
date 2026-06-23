from typing import Any

from pydantic import BaseModel, Field


class DashboardCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)


class WidgetCreate(BaseModel):
    query_history_id: int
    title: str = Field(min_length=2, max_length=255)
    chart_type: str = "bar"
    config_json: dict[str, Any] = Field(default_factory=dict)


class DashboardResponse(BaseModel):
    id: int
    name: str
    layout_json: dict[str, Any]

    class Config:
        from_attributes = True
