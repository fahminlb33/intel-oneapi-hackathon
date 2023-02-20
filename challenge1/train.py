import os
import time
import pickle
import logging
import argparse
import datetime

os.environ["__MODIN_AUTOIMPORT_PANDAS__"] = "1"
os.environ["RAY_verbose_spill_logs"] = "0"

# register logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# create argument parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("--backend",
                    type=str,
                    default="cpu",
                    choices=["cpu", "gpu"],
                    help="Select which backend to use")
parser.add_argument("--model-format",
                    type=str,
                    default="json",
                    choices=["json", "ubj", "daal4py"],
                    help="Select which model format to use")
parser.add_argument(
    "--best-params",
    action='store_true',
    help="Use best parameters defined in parameters.py for training")
parser.add_argument("--dataset",
                    type=str,
                    required=True,
                    help="Full path to dataset file (dataset.csv)")
parser.add_argument(
    "--output",
    type=str,
    required=True,
    help="Full path to output directory")

# parse args
args = parser.parse_args()

logging.info(f"Using backend: {args.backend}")
logging.info(f"Using model format: {args.model_format}")
logging.info(f"Using use best parameters: {args.best_params}")
logging.info(f"Using dataset: {args.dataset}")
logging.info(f"Using output directory: {args.output}")

# ----- imports
from sklearnex import patch_sklearn

patch_sklearn()

import ray

ray.init()

import numpy as np
import modin.pandas as pd

import xgboost as xgb
import daal4py as d4p

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from parameters import XGBOOST_PARAMS
from preprocess import load_data, preprocess

# constants and time measurement
TODAY = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
TIME_HISTORY = []

# ---- step 1: data loading
logging.info("Loading data...")
start_time = time.time()

df = load_data(args.dataset)

TIME_HISTORY.append({
    "action": "load_dataset",
    "elapsed": time.time() - start_time
})

# ---- step 2: data preprocessing
logging.info("Preprocessing...")
start_time = time.time()

df = preprocess(df)

TIME_HISTORY.append({
    "action": "prepare_dataset",
    "elapsed": time.time() - start_time
})

logging.info(f"Used columns: {df.columns}")

# ---- step 3: data splitting
logging.info("Splitting...")
start_time = time.time()

# split data, stratify by target
train_x, valid_x, train_y, valid_y = train_test_split(df.iloc[:, :-1],
                                                      df.iloc[:, -1],
                                                      stratify=df.iloc[:, -1],
                                                      test_size=.2,
                                                      random_state=42)

TIME_HISTORY.append({
    "action": "train_test_split",
    "elapsed": time.time() - start_time
})

# create DMatrix
dtrain = xgb.DMatrix(train_x, label=train_y)
dvalid = xgb.DMatrix(valid_x, label=valid_y)

# ---- step 4: model training
logging.info("Training...")
start_time = time.time()

# create parameters
train_params = {"objective": "binary:logistic"}
if args.best_params:
    train_params = {**train_params, **XGBOOST_PARAMS}

if args.backend == "gpu":
    train_params = {**train_params, **{"tree_method": "gpu_hist"}}

# run training
bst = xgb.train(train_params, dtrain)

TIME_HISTORY.append({
    "action": "training",
    "elapsed": time.time() - start_time
})

# ---- step 5: model evaluation
logging.info("Evaluating...")
start_time = time.time()

# run evaluation
preds = None
if args.model_format == "daal4py":
    daal_model = d4p.get_gbt_model_from_xgboost(bst)
    daal_compute = d4p.gbt_classification_prediction(nClasses=2)
    preds = daal_compute.compute(valid_x, daal_model).prediction
else:
    preds = bst.predict(dvalid)

TIME_HISTORY.append({
    "action": "evaluation",
    "elapsed": time.time() - start_time
})

# print metrics
pred_labels = np.rint(preds)
logging.info("Evaluation result:\n"+classification_report(valid_y, pred_labels))

# save run history
logging.info("Saving run history...")
out_path = os.path.join(args.output, f"runs-{TODAY}.csv")
df_stats = pd.DataFrame.from_dict(TIME_HISTORY, orient='columns')
df_stats.to_csv(out_path)

# ---- step 6: model saving
logging.info("Saving model...")

if args.model_format == "ubj":
    out_path = os.path.join(args.output, f"model-{TODAY}.ubj")
    bst.save_model(out_path)

if args.model_format == "json":
    out_path = os.path.join(args.output, f"model-{TODAY}.json")
    bst.save_model(out_path)

if args.model_format == "daal4py":
    out_path = os.path.join(args.output, f"model-{TODAY}.pkl")
    daal_model = d4p.get_gbt_model_from_xgboost(bst)
    with open(out_path, "wb") as f:
        pickle.dump(daal_model, f)
