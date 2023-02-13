import modin.pandas as pd

from parameters import LOAD_COLUMNS, COLOR_MAP, SOURCE_MAP, MONTH_MAP


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col="Index", names=LOAD_COLUMNS, skiprows=1)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Ordinal encoding for categorical columns
    df["color"] = df["color"].map(COLOR_MAP)
    df["source"] = df["source"].map(SOURCE_MAP)
    df["month"] = df["month"].map(MONTH_MAP)

    # Fill or drop missing values
    df = df.fillna(method="bfill")

    # Reorder columns
    original_columns = df.columns.tolist()
    original_columns.remove("target")
    df = df.reindex(columns=original_columns + ["target"])

    return df
