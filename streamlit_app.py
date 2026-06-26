import re
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


DATA_TABLE = "dataset"


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at 10% 5%, rgba(14,124,134,0.15), transparent 35%),
                    radial-gradient(circle at 90% 10%, rgba(54,164,123,0.12), transparent 30%),
                    linear-gradient(180deg, #f6f8f5 0%, #eef4f1 100%);
            }

            .hero-wrap {
                border-radius: 18px;
                padding: 1.25rem 1.4rem;
                background: linear-gradient(135deg, #0e7c86 0%, #2f9b75 100%);
                color: #f8fbfa;
                margin-bottom: 1rem;
                box-shadow: 0 12px 24px rgba(17, 56, 63, 0.18);
            }

            .hero-title {
                font-size: 1.85rem;
                line-height: 1.2;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }

            .hero-sub {
                font-size: 1.0rem;
                opacity: 0.96;
            }

            .metric-strip {
                display: flex;
                gap: 0.75rem;
                flex-wrap: wrap;
                margin-top: 0.9rem;
            }

            .metric-pill {
                background: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 999px;
                padding: 0.3rem 0.8rem;
                font-size: 0.9rem;
            }

            .section-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid #d7e3de;
                border-radius: 16px;
                padding: 0.9rem 1rem;
                box-shadow: 0 6px 18px rgba(31, 53, 43, 0.07);
                margin-bottom: 0.9rem;
            }

            .section-title {
                font-size: 1.1rem;
                font-weight: 700;
                color: #18333a;
                margin: 0 0 0.35rem 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero(df: pd.DataFrame) -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-title">AI SQL Agent Studio</div>
            <div class="hero-sub">Upload CSVs, ask in plain language, and explore data instantly with SQL.</div>
            <div class="metric-strip">
                <div class="metric-pill">Rows: {len(df)}</div>
                <div class="metric-pill">Columns: {len(df.columns)}</div>
                <div class="metric-pill">Engine: DuckDB</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _section_open(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _load_default_data() -> pd.DataFrame:
    sample_path = Path(__file__).resolve().parent / "sample-upload.csv"
    if sample_path.exists():
        return pd.read_csv(sample_path)
    return pd.DataFrame()


def _detect_columns(df: pd.DataFrame) -> tuple[list[str], list[str], list[str]]:
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    date_like_cols: list[str] = []
    category_cols: list[str] = []
    for col in df.columns:
        lower_col = str(col).lower()
        if col in numeric_cols:
            continue
        if "date" in lower_col or "time" in lower_col:
            date_like_cols.append(col)
        else:
            category_cols.append(col)
    return numeric_cols, date_like_cols, category_cols


def _match_column(prompt: str, columns: list[str]) -> str | None:
    prompt_lower = prompt.lower()
    for col in columns:
        if str(col).lower() in prompt_lower:
            return col
    return None


def _suggest_sql(prompt: str, df: pd.DataFrame) -> tuple[str, str]:
    normalized = prompt.strip().lower()
    cols = [str(c) for c in df.columns]
    numeric_cols, date_cols, category_cols = _detect_columns(df)

    if not cols:
        return "", "No columns found. Upload a CSV first."

    if "monthly" in normalized and date_cols and numeric_cols and ("sum" in normalized or "total" in normalized):
        date_col = _match_column(normalized, date_cols) or date_cols[0]
        metric_col = _match_column(normalized, numeric_cols) or numeric_cols[0]
        sql = (
            f"SELECT strftime(try_cast({date_col} AS DATE), '%Y-%m') AS month, "
            f"SUM({metric_col}) AS total_{metric_col} "
            f"FROM {DATA_TABLE} "
            "GROUP BY 1 ORDER BY 1"
        )
        return sql, "Detected a monthly trend query and generated month-wise aggregation."

    if "average" in normalized or "avg" in normalized or "mean" in normalized:
        metric_col = _match_column(normalized, numeric_cols) or (numeric_cols[0] if numeric_cols else None)
        group_col = _match_column(normalized, category_cols)
        if metric_col and group_col:
            sql = (
                f"SELECT {group_col}, AVG({metric_col}) AS avg_{metric_col} "
                f"FROM {DATA_TABLE} GROUP BY {group_col} ORDER BY avg_{metric_col} DESC"
            )
            return sql, "Calculated averages grouped by the category found in your prompt."
        if metric_col:
            sql = f"SELECT AVG({metric_col}) AS avg_{metric_col} FROM {DATA_TABLE}"
            return sql, "Calculated an overall average for the requested metric."

    if "sum" in normalized or "total" in normalized:
        metric_col = _match_column(normalized, numeric_cols) or (numeric_cols[0] if numeric_cols else None)
        group_col = _match_column(normalized, category_cols)
        if metric_col and group_col:
            sql = (
                f"SELECT {group_col}, SUM({metric_col}) AS total_{metric_col} "
                f"FROM {DATA_TABLE} GROUP BY {group_col} ORDER BY total_{metric_col} DESC"
            )
            return sql, "Summed values grouped by the category mentioned in your prompt."
        if metric_col:
            sql = f"SELECT SUM({metric_col}) AS total_{metric_col} FROM {DATA_TABLE}"
            return sql, "Calculated a total for the selected metric."

    if "count" in normalized:
        group_col = _match_column(normalized, category_cols)
        if group_col:
            sql = (
                f"SELECT {group_col}, COUNT(*) AS row_count "
                f"FROM {DATA_TABLE} GROUP BY {group_col} ORDER BY row_count DESC"
            )
            return sql, "Counted records by category."
        return f"SELECT COUNT(*) AS row_count FROM {DATA_TABLE}", "Counted total records."

    top_match = re.search(r"top\s+(\d+)", normalized)
    if top_match and numeric_cols:
        limit_n = int(top_match.group(1))
        metric_col = _match_column(normalized, numeric_cols) or numeric_cols[0]
        sql = f"SELECT * FROM {DATA_TABLE} ORDER BY {metric_col} DESC LIMIT {limit_n}"
        return sql, f"Returned top {limit_n} rows by {metric_col}."

    return f"SELECT * FROM {DATA_TABLE} LIMIT 100", "Used a safe default query because the prompt was broad."


def _run_sql(df: pd.DataFrame, sql: str) -> pd.DataFrame:
    con = duckdb.connect(database=":memory:")
    try:
        con.register(DATA_TABLE, df)
        return con.execute(sql).df()
    finally:
        con.close()


def _render_auto_chart(result_df: pd.DataFrame) -> None:
    if result_df.empty or len(result_df.columns) < 2:
        return

    first_col = result_df.columns[0]
    numeric_cols = [c for c in result_df.columns[1:] if pd.api.types.is_numeric_dtype(result_df[c])]
    if not numeric_cols:
        return

    y_col = numeric_cols[0]
    if any(token in str(first_col).lower() for token in ["date", "month", "year", "time"]):
        st.line_chart(result_df.set_index(first_col)[y_col])
    else:
        st.bar_chart(result_df.set_index(first_col)[y_col])


def main() -> None:
    st.set_page_config(page_title="AI SQL Agent", page_icon="📊", layout="wide")
    _inject_styles()

    with st.sidebar:
        st.header("Data Source")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        use_sample = st.button("Use Sample Data", use_container_width=True)

    if use_sample:
        st.session_state["dataset"] = _load_default_data()

    if uploaded_file is not None:
        st.session_state["dataset"] = pd.read_csv(uploaded_file)

    if "dataset" not in st.session_state:
        st.session_state["dataset"] = _load_default_data()

    df = st.session_state["dataset"]
    if df.empty:
        st.warning("No data loaded. Upload a CSV or click 'Use Sample Data'.")
        return

    _render_hero(df)

    _section_open("Dataset Preview", "Inspect your data before generating queries.")
    st.dataframe(df.head(20), use_container_width=True)

    _section_open("Ask in Natural Language", "Describe what you want, then generate and run SQL.")
    prompt = st.text_area(
        "Prompt",
        placeholder="Examples: total revenue by region, top 5 by revenue, monthly total revenue",
        height=100,
    )

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("Generate SQL", use_container_width=True)
    with col2:
        run_now = st.button("Run SQL", use_container_width=True)

    if generate:
        if len(prompt.strip()) < 2:
            st.error("Please enter a longer prompt.")
        else:
            sql, explanation = _suggest_sql(prompt, df)
            st.session_state["generated_sql"] = sql
            st.session_state["generated_explanation"] = explanation

    sql_to_run = st.text_area(
        "SQL Editor",
        value=st.session_state.get("generated_sql", f"SELECT * FROM {DATA_TABLE} LIMIT 100"),
        height=140,
    )

    explanation = st.session_state.get("generated_explanation")
    if explanation:
        st.info(explanation)

    if run_now:
        try:
            result_df = _run_sql(df, sql_to_run.strip())
        except Exception as exc:
            st.error(f"SQL execution failed: {exc}")
            return

        _section_open("Results", "Query output and chart are generated below.")
        st.dataframe(result_df, use_container_width=True)
        _render_auto_chart(result_df)

        csv_bytes = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results CSV", csv_bytes, file_name="query_results.csv", mime="text/csv")


if __name__ == "__main__":
    main()
