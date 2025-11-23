import pandas as pd

def _fmt(value):
    if isinstance(value, (int, float)):
        return f"{value:,.2f}"
    return str(value)

def compute_kpis(df: pd.DataFrame, preset: dict):
    kpis = []
    # Define targets
    y = preset.get("default_y")
    date_col = preset.get("default_x")
    cat_col = preset.get("primary_category")

    # Total metric
    if y in df.columns and pd.api.types.is_numeric_dtype(df[y]):
        total = df[y].sum()
        kpis.append(("Total " + (y.title()), _fmt(total), None))

        # Average metric
        avg = df[y].mean()
        kpis.append(("Average " + (y.title()), _fmt(avg), None))

        # Growth vs previous period (simple heuristic)
        if date_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            s = df.sort_values(date_col)
            half = len(s) // 2
            prev = s.iloc[:half][y].mean() if half > 0 else None
            curr = s.iloc[half:][y].mean() if half > 0 else None
            if prev and curr:
                delta_pct = ((curr - prev) / prev) * 100 if prev != 0 else None
                kpis.append(("Growth %", _fmt(delta_pct if delta_pct is not None else 0), f"{_fmt(curr - prev)} vs prev"))

    # Top category
    if cat_col in df.columns:
        top = df.groupby(cat_col)[y].sum().sort_values(ascending=False).head(1)
        if len(top) == 1:
            kpis.append(("Top " + cat_col.title(), top.index[0], _fmt(top.values[0])))

    # Row count
    kpis.append(("Rows", f"{len(df):,}", None))
    return kpis
