import os
import json
import requests
import numpy as np


def preprocess(img):
    img = img.resize((640, 640))
    img = np.array(img, dtype='float32')
    img = img.transpose(2, 0, 1)
    img = img / 255
    return img.reshape(1, 3, 640, 640)


def request_prediction(img):
    # get API url and model name
    api_url = os.environ.get("API_HOST")
    model_name = os.environ.get("MODEL_NAME")

    # build request body
    req_headers = {"content-type": "application/json"}
    req_data = json.dumps({
        "signature_name": "serving_default",
        "instances": img.tolist()
    })

    # send request
    api_response = requests.post(f"{api_url}/v1/models/{model_name}:predict",
                                 data=req_data,
                                 headers=req_headers)

    # get the prediction
    predictions = np.array(api_response.json()["predictions"])

    return predictions[0]
