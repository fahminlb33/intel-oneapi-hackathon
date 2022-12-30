import json
import requests
import numpy as np
from PIL import Image

# load image
img = Image.open('../dataset/cropweed-yolo/dataset/images/agri_0_14.jpeg')
img = img.resize((640, 640))
img = np.array(img, dtype='float32')
img = img.transpose(2,0,1)
img = img / 255
img = img.reshape(1,3,640,640)

print(img.shape, "; data range:",np.amin(img),":",np.amax(img))

# create predict request using request and load 
# the image as a json using tensorflow serving API
data = json.dumps({"signature_name": "serving_default", "instances": img.tolist()})
headers = {"content-type": "application/json"}
json_response = requests.post('http://localhost:9001/v1/models/model1:predict', data=data, headers=headers)

# get the prediction
predictions = np.array(json.loads(json_response.text)["predictions"])


import challenge2.web_app.nmr as nmr

result_boxes, result_scores, result_class_names = nmr.nms(predictions[0])

print("TOTAL: ", len(result_boxes))
for i in range(len(result_boxes)):
    print("Bounding box: ", result_boxes[i])
    print("Scores: ", result_scores[i])
    print("Classes: ", result_class_names[i])
