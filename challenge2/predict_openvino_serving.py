import json
import requests
import numpy as np

from PIL import Image

import app_web.nmr as nmr

# const
IMAGE_SIZE = 640
IMAGE_PATH = '../dataset/cropweed/dataset/images/agri_0_14.jpeg'
VINO_SERVER = 'http://localhost:9001/v1/models/challenge2:predict'

# load image
img_original = Image.open(IMAGE_PATH)

# preprocess image
img_original = img_original.resize((IMAGE_SIZE, IMAGE_SIZE))
img_original = np.array(img_original, dtype='float32')
img_original = img_original.transpose(2, 0, 1)
img_original = img_original / 255
img_original = img_original.reshape(1, 3, IMAGE_SIZE, IMAGE_SIZE)

# create predict request using requests
post_data = {
    "signature_name": "serving_default",
    "instances": img_original.tolist()
}
post_headers = {"content-type": "application/json"}
json_response = requests.post(VINO_SERVER,
                              data=json.dumps(post_data),
                              headers=post_headers)

# get the prediction
predictions = np.array(json_response.json()["predictions"])

# perform NMS
result_boxes, result_scores, result_class_names = nmr.nms(predictions[0])

# exit if no box found
if len(result_boxes) == 0:
    print("No boxes found")
    exit(0)

# print detection
print("TOTAL: ", len(result_boxes))
for i in range(len(result_boxes)):
    print("Bounding box: ", result_boxes[i])
    print("Scores: ", result_scores[i])
    print("Classes: ", result_class_names[i])

# load and 
img_pred = Image.open(IMAGE_PATH)
img_pred = nmr.draw_boxes(img_pred, result_boxes, result_scores, result_class_names)
img_pred.save('result-serving.png')
