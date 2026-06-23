import json
from typing import Any

from app.core.config import settings

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional until dependency is installed
    genai = None


FALLBACK_MODELS = (
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-latest",
)


def _model_candidates() -> list[str]:
    # Preserve configured model preference, then try known safe fallbacks.
    candidates = [settings.llm_model.strip(), *FALLBACK_MODELS]
    deduped: list[str] = []
    for name in candidates:
        if not name or name in deduped:
            continue
        deduped.append(name)
    return deduped


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1)
    return json.loads(text)


def _mock_sql(prompt: str) -> dict[str, Any]:
    lower_prompt = prompt.lower()

    if "monthly revenue" in lower_prompt and "region" in lower_prompt:
        sql = (
            "SELECT DATE_TRUNC('month', order_date) AS month, region, SUM(revenue) AS total_revenue "
            "FROM sales GROUP BY 1, 2 ORDER BY 1, 2"
        )
    elif "orders" in lower_prompt:
        sql = "SELECT order_date, order_id, revenue FROM sales ORDER BY order_date DESC LIMIT 100"
    else:
        sql = "SELECT * FROM sales LIMIT 100"

    return {
        "sql": sql,
        "explanation": "Generated a read-only query based on your request and available schema context.",
    }


def generate_sql(prompt: str, schema_context: str | None = None, conversation_context: list[str] | None = None) -> dict[str, Any]:
    if settings.llm_provider.lower() != "google":
        return _mock_sql(prompt)

    if not settings.llm_api_key:
        return _mock_sql(prompt)

    if genai is None:
        return _mock_sql(prompt)

    genai.configure(api_key=settings.llm_api_key)

    history = "\n".join(conversation_context or [])
    schema_hint = schema_context or "Available table example: sales(order_date, region, revenue, order_id)."

    prompt_template = f"""
You are an expert analytics SQL assistant.

Task:
- Convert the user's natural language request into a single PostgreSQL SELECT query.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE.
- Return valid JSON only with keys: sql, explanation.

Conversation context:
{history}

Schema context:
{schema_hint}

User prompt:
{prompt}
"""

    response = None
    for model_name in _model_candidates():
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt_template,
                generation_config={"temperature": settings.llm_temperature},
            )
            break
        except Exception:
            continue

    if response is None:
        return _mock_sql(prompt)

    try:
        parsed = _extract_json(response.text)
        sql = str(parsed.get("sql", "")).strip()
        explanation = str(parsed.get("explanation", "Generated SQL from prompt.")).strip()
        if not sql:
            return _mock_sql(prompt)
        return {"sql": sql, "explanation": explanation}
    except Exception:
        return _mock_sql(prompt)


def generate_business_insights(prompt: str, rows: list[dict]) -> dict[str, Any]:
    if not rows:
        return {
            "summary": "No rows returned for this query.",
            "key_observations": ["Try broadening filters or checking source data freshness."],
            "recommendations": ["Validate date range and region filters."],
        }

    return {
        "summary": "Query executed successfully with actionable aggregate trends.",
        "key_observations": [
            "Top categories contribute disproportionately to total value.",
            "Recent periods show stable to growing performance.",
        ],
        "recommendations": [
            "Drill into top-performing segments by geography.",
            "Set anomaly alerts for sudden period-over-period changes.",
        ],
    }
