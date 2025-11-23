import streamlit as st
import pandas as pd

def build_filters_ui(df: pd.DataFrame, preset: dict):
    filters = []

    # Suggested categorical filters
    for col in preset.get("categorical_filters", []):
        if col in df.columns:
            options = sorted(df[col].dropna().astype(str).unique().tolist())
            selected = st.multiselect(f"{col}", options)
            if selected:
                filters.append(("categorical_in", col, selected))

    # Suggested numeric range filters
    for col in preset.get("numeric_filters", []):
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            mn, mx = float(df[col].min()), float(df[col].max())
            selected = st.slider(f"{col} range", min_value=mn, max_value=mx, value=(mn, mx))
            filters.append(("numeric_range", col, selected))

    # Date range filter (optional)
    for col in preset.get("date_filters", []):
        if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
            min_date, max_date = df[col].min(), df[col].max()
            start, end = st.date_input(f"{col} period", (min_date, max_date))
            filters.append(("date_range", col, (start, end)))

    # Free-form column filter
    with st.expander("Advanced filters"):
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                pass  # keep UI simple; preset-driven filters usually suffice
    return filters

def apply_filters(df: pd.DataFrame, filters):
    out = df.copy()
    for ftype, col, val in filters:
        if ftype == "categorical_in":
            out = out[out[col].astype(str).isin(val)]
        elif ftype == "numeric_range":
            lo, hi = val
            out = out[(out[col] >= lo) & (out[col] <= hi)]
        elif ftype == "date_range":
            start, end = pd.to_datetime(val[0]), pd.to_datetime(val[1])
            out = out[(out[col] >= start) & (out[col] <= end)]
    return out
