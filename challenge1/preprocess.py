import modin.pandas as pd

COLOR_MAP = {
    "Yellow": 0,
    "Light Yellow": 1,
    "Faint Yellow": 2,
    "Near Colorless": 3,
    "Colorless": 4
}

SOURCE_MAP = {
    "Lake": 0,
    "Spring": 1,
    "River": 2,
    "Reservoir": 3,
    "Aquifer": 4,
    "Well": 5,
    "Ground": 6,
    "Stream": 7,
}

MONTH_MAP = {
    "January": 0,
    "February": 1,
    "March": 2,
    "April": 3,
    "May": 4,
    "June": 5,
    "July": 6,
    "August": 7,
    "September": 8,
    "October": 9,
    "November": 10,
    "December": 11
}

LOAD_COLUMNS = [
    "Index",
    "ph",
    "iron",
    "nitrate",
    "chloride",
    "lead",
    "zinc",
    "color",
    "turbidity",
    "fluoride",
    "copper",
    "odor",
    "sulfate",
    "conductivity",
    "chlorine",
    "manganese",
    "total_dissolved_solids",
    "source",
    "water_temperature",
    "air_temperature",
    "month",
    "day",
    "time_of_day",
    "target",
]


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
