import pandas as pd
import math
from .utils import load_dataset

_df = load_dataset()

def _safe_mean(series):
    if series is None or len(series.dropna()) == 0:
        return None
    m = series.dropna().mean()
    # if mean is NaN/inf, return None so JSON can serialize it
    if pd.isna(m) or (isinstance(m, float) and (math.isnan(m) or math.isinf(m))):
        return None
    return float(m)

def _top_counts(df, col):
    if col not in df.columns:
        return {}
    # ensure strings and drop empties, then convert counts to plain ints
    vc = df[col].astype(str).replace({"nan": ""}).replace({"None": ""}).replace({"": None}).dropna()
    return {str(k): int(v) for k, v in vc.value_counts().head(10).items()}

def summary():
    df = _df.copy()
    # price column may be text; coerce to numeric safely
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    return {
        "n_items": int(len(df)),
        "avg_price": _safe_mean(df["price"]) if "price" in df.columns else None,
        "top_brands": _top_counts(df, "brand"),
        "top_categories": _top_counts(df, "categories"),
        "colors": _top_counts(df, "color"),
    }
