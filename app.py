import streamlit as st
import pandas as pd
from modules.data_loader import load_file
from modules.filters import build_filters_ui, apply_filters
from modules.kpis import compute_kpis
from modules.charts import build_chart_ui, render_chart
from modules.report import make_download_buttons
from config import INDUSTRY_PRESETS, THEME

st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar: Industry + Upload
with st.sidebar:
    st.header("⚙️ Controls")
    industry = st.selectbox("Industry", list(INDUSTRY_PRESETS.keys()))
    st.caption("Pick industry to auto-map KPIs and chart options.")
    uploaded = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

    st.divider()
    st.markdown("**Chart Settings**")
    chart_type = build_chart_ui()

st.title("📊 Data Dashboard")
st.caption("Upload data, filter, explore KPIs, and download reports.")

if not uploaded:
    st.info("Upload a CSV or Excel file to begin.")
    st.stop()

# Load data
df = load_file(uploaded)
if df is None or df.empty:
    st.error("Failed to load data or file is empty.")
    st.stop()

# Presets for selected industry
preset = INDUSTRY_PRESETS[industry]

# Data preview
with st.expander("Data preview"):
    st.dataframe(df.head(200), use_container_width=True)

# Filters
with st.sidebar:
    st.divider()
    st.markdown("**Filters**")
    user_filters = build_filters_ui(df, preset)

filtered_df = apply_filters(df, user_filters)

# KPIs row
kpi_values = compute_kpis(filtered_df, preset)
kpi_cols = st.columns(min(4, max(1, len(kpi_values))))
for i, (label, value, delta) in enumerate(kpi_values):
    with kpi_cols[i % len(kpi_cols)]:
        st.metric(label=label, value=value, delta=delta)

st.divider()

# Chart area
left, right = st.columns([3, 2])
with left:
    x_col, y_col = preset.get("default_x"), preset.get("default_y")
    if x_col not in filtered_df.columns:
        x_col = filtered_df.columns[0]
    if y_col not in filtered_df.columns:
        # pick first numeric col
        numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
        y_col = numeric_cols[0] if numeric_cols else filtered_df.columns[-1]

    fig = render_chart(filtered_df, chart_type, x_col=x_col, y_col=y_col)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Download")
    make_download_buttons(filtered_df, industry)

# Footer
st.caption(THEME["footer_note"])
