import time

import numpy as np
import pandas as pd

import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from parameters import XGBOOST_PARAMS

time_measures = []

print("Loading data...")
start_time = time.time()
df = pd.read_csv("../dataset/freshwater/dataset.csv", index_col="Index").dropna()
time_measures.append({"action": "load_dataset", "elapsed": time.time() - start_time})

print("Preprocessing...")
start_time = time.time()

df_nona = df.drop(columns=["Month", "Day", "Time of Day"])
df_nona["Color"] = df_nona["Color"].astype("category")
df_nona["Source"] = df_nona["Source"].astype("category")

df_cat = pd.get_dummies(data=df_nona, columns=["Color", "Source"])

original_columns = df_cat.columns.tolist()
original_columns.remove("Target")
df_cat = df_cat.reindex(columns=original_columns + ["Target"])

time_measures.append({"action": "prepare_dataset", "elapsed": time.time() - start_time})

print("Splitting...")
start_time = time.time()
train_x, valid_x, train_y, valid_y = train_test_split(df_cat.iloc[:, :-1], df_cat.iloc[:, -1], stratify=df_cat.iloc[:, -1], test_size=.2, random_state=42)
time_measures.append({"action": "train_test_split", "elapsed": time.time() - start_time})

dtrain = xgb.DMatrix(train_x, label=train_y)
dvalid = xgb.DMatrix(valid_x, label=valid_y)

print("Training...")
start_time = time.time()
bst = xgb.train({**XGBOOST_PARAMS, "tree_method": "gpu_hist", "gpu_id": 0}, dtrain)
time_measures.append({"action": "training", "elapsed": time.time() - start_time})

print("Evaluating...")
start_time = time.time()
preds = bst.predict(dvalid)
time_measures.append({"action": "evaluation", "elapsed": time.time() - start_time})

bst.save_model("models/gpu.ubj")
bst.save_model("models/gpu.json")

pred_labels = np.rint(preds)

print(classification_report(valid_y, pred_labels))

df_stats = pd.DataFrame.from_dict(time_measures, orient='columns')
df_stats.to_csv("models/gpu.csv")
print(df_stats)
