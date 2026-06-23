from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import AuditLog, QueryHistory, User
from app.schemas.chat import ChatResponse
from app.services.llm_service import generate_business_insights, generate_sql
from app.services.sql_runner import execute_sql
from app.services.sql_safety import validate_readonly_sql
from app.services.visualization_service import detect_chart


def _json_safe(value):
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def process_chat(prompt: str, db: Session, user: User) -> ChatResponse:
    last_prompts = [
        item.prompt
        for item in db.query(QueryHistory)
        .filter(QueryHistory.user_id == user.id)
        .order_by(QueryHistory.id.desc())
        .limit(5)
    ]

    llm_output = generate_sql(prompt=prompt, conversation_context=last_prompts)
    sql = llm_output["sql"]

    try:
        safe_sql = validate_readonly_sql(sql)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        rows, columns, execution_ms = execute_sql(db, safe_sql)
    except Exception as exc:
        db.add(AuditLog(user_id=user.id, action="query_failed", details={"error": "execution_error"}))
        db.commit()
        raise HTTPException(status_code=400, detail="Query execution failed. The query was retried and still invalid.") from exc

    insights = generate_business_insights(prompt, rows)
    chart = detect_chart(columns, rows)

    safe_rows = _json_safe(rows)
    safe_chart = _json_safe(chart)

    history = QueryHistory(
        user_id=user.id,
        prompt=prompt,
        sql_text=safe_sql,
        explanation=llm_output.get("explanation", ""),
        insight_summary=insights["summary"],
        chart_type=chart["type"],
        execution_ms=execution_ms,
        row_count=len(rows),
        result_json={"columns": columns, "rows": safe_rows, "chart": safe_chart},
    )
    db.add(history)
    db.add(AuditLog(user_id=user.id, action="query_executed", details={"prompt": prompt, "rows": len(rows)}))
    db.commit()

    return ChatResponse(
        prompt=prompt,
        sql=safe_sql,
        explanation=llm_output.get("explanation", ""),
        insight_summary=insights["summary"],
        key_observations=insights["key_observations"],
        recommendations=insights["recommendations"],
        rows=safe_rows,
        columns=columns,
        chart=safe_chart,
        execution_ms=execution_ms,
        timestamp=datetime.now(timezone.utc),
    )
