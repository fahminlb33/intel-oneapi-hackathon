import os
import json
import base64
import requests
import numpy as np

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, render_template

import app_web.nmr as nmr

app = Flask(__name__)

def draw_boxes(file, result_boxes, result_scores, result_class_names):
    # load file
    image = Image.open(file)

    # return original image if no boxes are found
    if len(result_boxes) == 0:
        return image

    # scale boxes
    original_size = image.size[:2]
    result_boxes = nmr.scale_coords((640, 640), np.array(result_boxes), (original_size[1], original_size[0]))

    # create image drawing object
    img_draw = ImageDraw.Draw(image)

    # draw boxes
    for i, r in enumerate(result_boxes):
        # draw rectangle
        rect_start = (int(r[0]), int(r[1]))
        rect_end = (int(r[2]), int(r[3]))
        img_draw.rectangle(rect_start, rect_end, fill="red")

        # draw text
        text_org = (int(r[0]), int(r[1]))
        text_content = f"{100*result_scores[i]:.0}% {result_class_names[i]}"
        img_draw.text(text_content, text_org, font=ImageFont.truetype("arial"))
        
    return image

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/prediction", methods=["POST"])
def prediction():
    # get API url and model name
    api_url = os.environ.get("API_URL")
    model_name = os.environ.get("MODEL_NAME")

    # load uploaded file
    uploaded_file = request.files["file"]
    
    # load image to Pillow
    img = Image.open(uploaded_file)

    # preprocess image
    img = img.resize((640, 640))
    img = np.array(img, dtype='float32')
    img = img.transpose(2,0,1)
    img = img / 255
    img = img.reshape(1, 3, 640, 640)

    # send request to OpenVINO Serving
    req_data = json.dumps({"signature_name": "serving_default", "instances": img.tolist()})
    req_headers = {"content-type": "application/json"}
    api_response = requests.post(f"{api_url}/v1/models/{model_name}:predict", data=req_data, headers=req_headers)

    # get the prediction
    predictions = np.array(json.loads(api_response.text)["predictions"])

    # get the prediction
    result_boxes, result_scores, result_class_names = nmr.nms(predictions[0])

    # draw boxes, if any
    img_annotated = draw_boxes(uploaded_file, result_boxes, result_scores, result_class_names)

    # convert uploaded file to base64
    buffered = BytesIO()
    img_annotated.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf8')

    return render_template("prediction.html", image=img_base64)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 9000)), debug=True)
