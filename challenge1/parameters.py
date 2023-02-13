XGBOOST_PARAMS = {
    "objective": "binary:logistic",
    "alpha": 0.0005072707539427799,
    "booster": "dart",
    "colsample_bytree": 0.9634270709794632,
    "eta": 9.843453637361607e-07,
    "eval_metric": "auc",
    "gamma": 0.016649678927282842,
    "grow_policy": "depthwise",
    "lambda": 0.8202866930443937,
    "max_depth": 9,
    "min_child_weight": 2,
    "normalize_type": "forest",
    "rate_drop": 0.0001395383872069001,
    "sample_type": "uniform",
    "skip_drop": 0.26622177133895697,
    "subsample": 0.5974172526635755,
}

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
