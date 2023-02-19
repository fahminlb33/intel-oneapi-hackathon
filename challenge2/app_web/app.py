import os
import base64

from io import BytesIO
from PIL import Image
from flask import Flask, request, render_template, send_file

import nmr as nmr
import predictor as predictor

app = Flask(__name__)


@app.route("/")
def index():
    show_app_menu = os.environ.get("SHOW_APP_MENU", "false").lower() == "true"
    return render_template("upload.html", show_app_menu=show_app_menu)


@app.route("/prediction", methods=["POST"])
def prediction():
    # load uploaded file
    uploaded_file = request.files["file"]

    # load image to Pillow
    img = Image.open(uploaded_file)

    # preprocess image
    img = predictor.preprocess(img)

    # send request to OpenVINO Serving
    pred_result = predictor.request_prediction(img)

    # get the prediction
    result_boxes, result_scores, result_class_names = nmr.nms(pred_result)

    # load image to Pillow
    img_annotated = Image.open(uploaded_file)

    # draw boxes, if any
    img_annotated = nmr.draw_boxes(img_annotated, result_boxes, result_scores,
                                   result_class_names)

    # exit if no box found
    if len(result_boxes) == 0:
        return render_template("prediction.html", image=None)

    # convert uploaded file to base64
    buffered = BytesIO()
    img_annotated.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf8')

    # create list of boxes
    found_items = []
    for i, r in enumerate(result_boxes):
        found_items.append({
            "rect": "({:.2f}, {:.2f}), ({:.2f}, {:.2f})".format(r[0], r[1], r[2], r[3]),
            "prediction": result_class_names[i],
            "confidence": "{:.2f}%".format(100 * result_scores[i])
        })
        
    return render_template("prediction.html", image=img_base64, found_items=found_items)


@app.route("/predict", methods=["POST"])
def prediction_api():
    # load uploaded file
    uploaded_file = request.files["file"]

    # load image to Pillow
    img = Image.open(uploaded_file)

    # preprocess image
    img = predictor.preprocess(img)

    # send request to OpenVINO Serving
    pred_result = predictor.request_prediction(img)

    # get the prediction
    result_boxes, result_scores, result_class_names = nmr.nms(pred_result)

    # exit if no box found
    if len(result_boxes) == 0:
        return "", 204

    # load image to Pillow
    img_annotated = Image.open(uploaded_file)

    # draw boxes, if any
    img_annotated = nmr.draw_boxes(img_annotated, result_boxes, result_scores,
                                   result_class_names)
    
    # save to buffer as JPG
    buffered = BytesIO()
    img_annotated.save(buffered, as_attachment=True, format="JPEG")
    
    # seek to beginning of file
    buffered.seek(0)

    return send_file(buffered, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8002)), debug=True)
