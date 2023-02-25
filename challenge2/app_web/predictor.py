import os
import json
import requests
import numpy as np
from ovmsclient import make_grpc_client

class Predictor:
    model_name: str
    rest_api_host: str
    grpc_client: None

    def __init__(self):
        self.model_name = os.environ.get("MODEL_NAME", "challenge2")
        self.rest_api_host = os.environ.get("REST_API_HOST", "http://localhost:9001")
        self.grpc_client = make_grpc_client(os.environ.get("GRPC_API_HOST", "localhost:9000"))


    def preprocess(self, img):
        img = img.resize((640, 640))
        img = np.array(img, dtype='float32')
        img = img.transpose(2, 0, 1)
        img = img / 255
        return img.reshape(1, 3, 640, 640)


    def request_prediction_rest(self, img):
        # build request body
        req_headers = {"content-type": "application/json"}
        req_data = json.dumps({
            "signature_name": "serving_default",
            "instances": img.tolist()
        })

        # send request
        api_response = requests.post(f"{self.rest_api_host}/v1/models/{self.model_name}:predict",
                                    data=req_data,
                                    headers=req_headers)

        # get the prediction
        predictions = np.array(api_response.json()["predictions"])

        return predictions[0]
    
    def request_prediction_grpc(self, img):
        predictions = self.grpc_client.predict(model_name=self.model_name, inputs={"images": img})
        return predictions[0]
