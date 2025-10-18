# backend/app/utils.py
import os
import pandas as pd

DATA_PATH = os.environ.get(
    "DATA_PATH",
    os.path.join(os.path.dirname(__file__), "data", "intern_data_ikarus.csv"),
)

def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Basic cleaning
    for col in ["title", "brand", "description", "categories",
                "material", "color", "manufacturer", "country_of_origin"]:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")

    # Clean price like "$1,299.00" -> "1299.00" then numeric
    if "price" in df.columns:
        df["price"] = (
            df["price"].astype(str)
            .str.replace(r"[^0-9.\-]", "", regex=True)
            .replace({"": None})
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    return df

