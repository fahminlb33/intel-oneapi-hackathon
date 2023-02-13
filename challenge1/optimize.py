import numpy as np
import xgboost as xgb

import mlflow
import optuna
from optuna.integration.mlflow import MLflowCallback
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from preprocess import load_data, preprocess

mlflc = MLflowCallback(
    tracking_uri="http://localhost:5000",
    metric_name=["accuracy", "f1"],
)


@mlflc.track_in_mlflow()
def objective(trial):
    print("Loading data...")
    df = load_data("../dataset/freshwater/dataset.csv")

    print("Preprocessing...")
    df = preprocess(df)

    print("Splitting...")
    train_x, valid_x, train_y, valid_y = train_test_split(df.iloc[:, :-1],
                                                          df.iloc[:, -1],
                                                          stratify=df.iloc[:,
                                                                           -1],
                                                          test_size=.2,
                                                          random_state=42)

    dtrain = xgb.DMatrix(train_x, label=train_y)
    dvalid = xgb.DMatrix(valid_x, label=valid_y)

    param = {
        "verbosity":
        0,
        "objective":
        "binary:logistic",
        "tree_method":
        "gpu_hist",
        "gpu_id":
        0,
        "eval_metric":
        "auc",
        # defines booster, gblinear for linear functions.
        "booster":
        trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"]),
        # L2 regularization weight.
        "lambda":
        trial.suggest_float("lambda", 1e-8, 1.0, log=True),
        # L1 regularization weight.
        "alpha":
        trial.suggest_float("alpha", 1e-8, 1.0, log=True),
        # sampling ratio for training data.
        "subsample":
        trial.suggest_float("subsample", 0.2, 1.0),
        # sampling according to each tree.
        "colsample_bytree":
        trial.suggest_float("colsample_bytree", 0.2, 1.0),
    }

    if param["booster"] in ["gbtree", "dart"]:
        # maximum depth of the tree, signifies complexity of the tree.
        param["max_depth"] = trial.suggest_int("max_depth", 3, 9, step=2)
        # minimum child weight, larger the term more conservative the tree.
        param["min_child_weight"] = trial.suggest_int("min_child_weight", 2,
                                                      10)
        param["eta"] = trial.suggest_float("eta", 1e-8, 1.0, log=True)
        # defines how selective algorithm is.
        param["gamma"] = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
        param["grow_policy"] = trial.suggest_categorical(
            "grow_policy", ["depthwise", "lossguide"])

    if param["booster"] == "dart":
        param["sample_type"] = trial.suggest_categorical(
            "sample_type", ["uniform", "weighted"])
        param["normalize_type"] = trial.suggest_categorical(
            "normalize_type", ["tree", "forest"])
        param["rate_drop"] = trial.suggest_float("rate_drop",
                                                 1e-8,
                                                 1.0,
                                                 log=True)
        param["skip_drop"] = trial.suggest_float("skip_drop",
                                                 1e-8,
                                                 1.0,
                                                 log=True)

    mlflow.log_params(param)

    print("Training...")
    bst = xgb.train(param, dtrain)

    print("Predict...")
    preds = bst.predict(dvalid)
    pred_labels = np.rint(preds)

    mlflow.xgboost.log_model(bst, "model.bin")

    return accuracy_score(valid_y, pred_labels), f1_score(valid_y, pred_labels)


if __name__ == "__main__":
    mlflow.set_experiment("xgboost")

    study = optuna.create_study(study_name="xgboost",
                                directions=["maximize", "maximize"],
                                storage="sqlite:///xgboost-history.db",
                                load_if_exists=True)

    study.optimize(objective, n_trials=50, callbacks=[mlflc])

    print("Number of finished trials: ", len(study.trials))
    print("Best trial:")
