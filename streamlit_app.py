import re
from datetime import datetime
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

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #dfe8e3 0%, #d5e2dc 100%);
                border-right: 1px solid #c3d4cc;
            }

            [data-testid="stSidebar"] > div:first-child {
                position: relative;
                overflow: hidden;
            }

            [data-testid="stSidebar"] > div:first-child::before {
                content: "";
                position: absolute;
                width: 210px;
                height: 210px;
                top: -75px;
                left: -65px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(20, 143, 152, 0.28) 0%, rgba(20, 143, 152, 0) 70%);
                animation: floatGlow 7s ease-in-out infinite;
                pointer-events: none;
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p {
                color: #12353d;
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"] {
                border: 1px solid #b9d2c8;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.55);
                padding: 0.35rem;
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
                border: 1px dashed #7db4a4;
                border-radius: 10px;
                animation: pulseBorder 2.6s ease-in-out infinite;
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
                border-radius: 10px;
                border: 1px solid #89b9aa;
                color: #0f4d57;
                background: #eef8f4;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 14px rgba(26, 83, 73, 0.18);
            }

            [data-testid="stSidebar"] [data-testid="stButton"] button {
                background: linear-gradient(135deg, #148f98 0%, #32a87a 100%);
                border: 1px solid #2f8e89;
                color: #f4fffb;
                box-shadow: 0 8px 16px rgba(20, 82, 75, 0.18);
                transition: all 0.22s ease;
            }

            [data-testid="stSidebar"] [data-testid="stButton"] button:hover {
                filter: brightness(1.05);
                transform: translateY(-1px) scale(1.01);
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

            [data-testid="stTextArea"] textarea {
                background: linear-gradient(180deg, #ffffff 0%, #f7fcfa 100%);
                border: 2px solid #84b8a9;
                border-radius: 14px;
                color: #143036;
                font-size: 0.98rem;
                box-shadow: 0 6px 14px rgba(19, 63, 53, 0.08);
            }

            [data-testid="stTextArea"] textarea:focus {
                border: 2px solid #0e7c86;
                box-shadow: 0 0 0 0.2rem rgba(14, 124, 134, 0.18);
            }

            [data-testid="stTextArea"] label p {
                color: #0d5661;
                font-weight: 700;
            }

            [data-testid="stButton"] button {
                border-radius: 12px;
                border: 1px solid #8fb7ab;
                background: linear-gradient(135deg, #0e7c86 0%, #2f9b75 100%);
                color: #f5fbf9;
                font-weight: 700;
            }

            [data-testid="stButton"] button:hover {
                border: 1px solid #0e7c86;
                filter: brightness(1.03);
            }

            .hint-card {
                border-radius: 14px;
                border: 1px dashed #87b2a8;
                background: rgba(242, 250, 247, 0.9);
                padding: 0.75rem 0.95rem;
                margin-bottom: 0.9rem;
            }

            .hint-chip {
                display: inline-block;
                margin: 0.18rem 0.2rem;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: #e2f2ee;
                border: 1px solid #b7d9d0;
                color: #17545e;
                font-size: 0.86rem;
            }

            .sidebar-card {
                border-radius: 14px;
                padding: 0.7rem 0.8rem;
                border: 1px solid #a8c8bd;
                background: linear-gradient(145deg, rgba(255,255,255,0.75) 0%, rgba(230,243,238,0.82) 100%);
                margin: 0.4rem 0 0.8rem 0;
            }

            .sidebar-card-title {
                font-weight: 700;
                color: #0f4a55;
                margin-bottom: 0.25rem;
                font-size: 0.95rem;
            }

            .sidebar-chip {
                display: inline-block;
                margin: 0.15rem 0.15rem 0 0;
                padding: 0.2rem 0.45rem;
                border-radius: 999px;
                border: 1px solid #b7d9d0;
                background: #edf8f3;
                color: #135862;
                font-size: 0.76rem;
            }

            @keyframes floatGlow {
                0% { transform: translateY(0px) translateX(0px); opacity: 0.7; }
                50% { transform: translateY(14px) translateX(12px); opacity: 1; }
                100% { transform: translateY(0px) translateX(0px); opacity: 0.7; }
            }

            @keyframes pulseBorder {
                0% { box-shadow: 0 0 0 0 rgba(20, 143, 152, 0.0); }
                50% { box-shadow: 0 0 0 4px rgba(20, 143, 152, 0.09); }
                100% { box-shadow: 0 0 0 0 rgba(20, 143, 152, 0.0); }
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


def _render_dataset_preview(df: pd.DataFrame) -> None:
    total_cells = max(len(df) * max(len(df.columns), 1), 1)
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2)

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns)}")
    c3.metric("Missing", f"{missing_cells:,}")
    c4.metric("Missing %", f"{missing_pct}%")

    tab1, tab2, tab3, tab4 = st.tabs(["Preview", "Data Quality", "Column Insights", "Highlights"])

    with tab1:
        st.dataframe(df.head(20), use_container_width=True)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Current Dataset", csv_bytes, file_name="dataset.csv", mime="text/csv")

    with tab2:
        quality_df = pd.DataFrame(
            {
                "column": df.columns,
                "dtype": [str(df[col].dtype) for col in df.columns],
                "missing_count": [int(df[col].isna().sum()) for col in df.columns],
                "missing_pct": [round(float(df[col].isna().mean() * 100), 2) for col in df.columns],
                "unique_values": [int(df[col].nunique(dropna=True)) for col in df.columns],
            }
        )
        st.dataframe(quality_df, use_container_width=True)

    with tab3:
        if numeric_cols:
            st.write("Numeric columns summary")
            st.dataframe(df[numeric_cols].describe().transpose(), use_container_width=True)
        else:
            st.info("No numeric columns found.")

        if cat_cols:
            pick_col = st.selectbox("See top values for a categorical column", options=cat_cols, key="cat_pick")
            top_vals = (
                df[pick_col]
                .astype("string")
                .fillna("<missing>")
                .value_counts()
                .head(10)
                .rename_axis("value")
                .reset_index(name="count")
            )
            st.dataframe(top_vals, use_container_width=True)
        else:
            st.info("No categorical columns found.")

    with tab4:
        if numeric_cols:
            sums = df[numeric_cols].sum(numeric_only=True).sort_values(ascending=False)
            top_metrics = sums.head(5).rename_axis("metric").reset_index(name="value")
            st.write("Top numeric totals")
            st.dataframe(top_metrics, use_container_width=True)
        else:
            st.info("Add numeric columns in your dataset to see highlights.")


def _render_sidebar_summary(df: pd.DataFrame) -> None:
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    missing_pct = round(float(df.isna().mean().mean() * 100), 2) if not df.empty else 0.0
    quality = max(0, int(100 - min(missing_pct, 100)))

    st.markdown(
        f"""
        <div class="sidebar-card">
            <div class="sidebar-card-title">Dataset Snapshot</div>
            <div><span class="sidebar-chip">Rows: {len(df):,}</span><span class="sidebar-chip">Cols: {len(df.columns)}</span></div>
            <div><span class="sidebar-chip">Numeric: {len(numeric_cols)}</span><span class="sidebar-chip">Quality: {quality}/100</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_quick_prompt_buttons() -> None:
    st.markdown("### Quick Prompts")
    quick_prompts = [
        "total revenue by region",
        "top 5 orders by revenue",
        "monthly total revenue",
        "average revenue by product",
    ]
    for idx, qp in enumerate(quick_prompts):
        if st.button(qp.title(), key=f"quick_prompt_{idx}", use_container_width=True):
            st.session_state["prompt_text"] = qp


def _render_query_history_sidebar() -> None:
    st.markdown("### Query History")
    history = st.session_state.get("query_history", [])
    if not history:
        st.caption("Run a query to build history.")
        return

    for idx, item in enumerate(history[:5]):
        with st.expander(f"{item['time']} | {item['rows']} rows"):
            st.write(item["prompt"])
            st.code(item["sql"], language="sql")
            if st.button("Reuse", key=f"reuse_{idx}", use_container_width=True):
                st.session_state["prompt_text"] = item["prompt"]
                st.session_state["generated_sql"] = item["sql"]
                st.rerun()


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

    if "query_history" not in st.session_state:
        st.session_state["query_history"] = []
    if "prompt_text" not in st.session_state:
        st.session_state["prompt_text"] = ""

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

    with st.sidebar:
        _render_sidebar_summary(df)
        _render_quick_prompt_buttons()
        _render_query_history_sidebar()

    _render_hero(df)

    _section_open("Dataset Preview", "Inspect your data before generating queries.")
    _render_dataset_preview(df)

    _section_open("Ask in Natural Language", "Describe what you want, then generate and run SQL.")
    st.markdown(
        """
        <div class="hint-card">
            <strong>Try these prompt ideas:</strong><br/>
            <span class="hint-chip">total revenue by region</span>
            <span class="hint-chip">top 5 orders by revenue</span>
            <span class="hint-chip">monthly total revenue</span>
            <span class="hint-chip">average revenue by product</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    prompt = st.text_area(
        "Prompt",
        key="prompt_text",
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

        st.session_state["query_history"] = [
            {
                "time": datetime.now().strftime("%H:%M"),
                "prompt": prompt.strip() or "Manual SQL run",
                "sql": sql_to_run.strip(),
                "rows": int(len(result_df)),
            }
        ] + st.session_state["query_history"]

        _section_open("Results", "Query output and chart are generated below.")
        st.dataframe(result_df, use_container_width=True)
        _render_auto_chart(result_df)

        csv_bytes = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results CSV", csv_bytes, file_name="query_results.csv", mime="text/csv")


if __name__ == "__main__":
    main()
