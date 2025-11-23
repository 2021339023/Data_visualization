import pandas as pd

def _basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Strip column names, unify whitespace, attempt to parse dates
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.columns:
        if df[col].dtype == object:
            # Trim string fields
            df[col] = df[col].astype(str).str.strip()
        # Try date parsing on likely date columns
        if any(k in col.lower() for k in ["date", "time", "day"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass
    return df

def load_file(uploaded_file):
    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="utf-8", low_memory=False)
        elif name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            return None
        df = _basic_clean(df)
        return df
    except Exception:
        return None
