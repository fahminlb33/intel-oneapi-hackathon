import os
import pickle
from datetime import datetime

import numpy as np
import daal4py as d4p

from flask import Flask, request, render_template

app = Flask(__name__,
            static_url_path='/assets',
            static_folder='assets',
            template_folder='templates')

# load model from daal4py file
model = None
predictor = None
with open("./data/oneapi-daal4py.pkl", "rb") as f:
    model = pickle.load(f)
    predictor = d4p.gbt_classification_prediction(
        nClasses=2,
        resultsToEvaluate="computeClassLabels|computeClassProbabilities")

FEATURE_NAMES = [
    "ph", "iron", "nitrate", "chloride", "lead", "zinc", "color", "turbidity",
    "fluoride", "copper", "odor", "sulfate", "conductivity", "chlorine",
    "manganese", "total_dissolved_solids", "source", "water_temperature",
    "air_temperature", "month", "day", "time_of_day"
]


@app.route("/")
def index():
    show_app_menu = os.environ.get("SHOW_APP_MENU", "false").lower() == "true"
    app_root_url = os.environ.get("APP_ROOT_URL", "http://locahost:8000")
    return render_template("form_inputs.html", show_app_menu=show_app_menu, app_root_url=app_root_url)


@app.route("/summary")
def summary():
    return render_template("summary.html")


@app.route("/prediction", methods=["POST"])
def prediction():
    pred_date = datetime.strptime(request.form["date"], '%Y-%m-%dT%H:%M')
    pred_data_raw = [
        request.form["ph"],
        request.form["iron"],
        request.form["nitrate"],
        request.form["chloride"],
        request.form["lead"],
        request.form["zinc"],
        request.form["color"],
        request.form["turbidity"],
        request.form["fluoride"],
        request.form["copper"],
        request.form["odor"],
        request.form["sulfate"],
        request.form["conductivity"],
        request.form["chlorine"],
        request.form["manganese"],
        request.form["total_dissolved_solids"],
        request.form["source"],
        request.form["water_temperature"],
        request.form["air_temperature"],
        pred_date.month,
        pred_date.day,
        pred_date.hour,
    ]

    pred_data = np.array(pred_data_raw).astype(np.float64).reshape(1, -1)
    preds = predictor.compute(pred_data, model)

    is_dangerous = preds.prediction[0] == 1
    probability = np.round(
        preds.probabilities[0][int(preds.prediction[0])] * 100, 2)

    return render_template("prediction.html",
                           is_dangerous=is_dangerous,
                           probability=probability)


@app.route("/predict", methods=["POST"])
def predict_json():
    data = request.get_json()
    pred_data = np.array(list(data.values())).astype(np.float64).reshape(1, -1)
    preds = predictor.compute(pred_data, model)

    result = {}
    for i, key in enumerate(data.keys()):
        result[key] = preds.probabilities[i].tolist()

    print(result)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))
