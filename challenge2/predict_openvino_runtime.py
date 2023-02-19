import numpy as np
import openvino.runtime as ov

from PIL import Image

import app_web.nmr as nmr

# const
IMAGE_SIZE = 640
IMAGE_PATH = '../dataset/cropweed/dataset/images/agri_0_14.jpeg'
MODEL_PATH = "./models/best.onnx"

# create openvin runtime
core = ov.Core()

# load and compile model
compiled_model = core.compile_model(MODEL_PATH, "AUTO")

# create infer request
infer_request = compiled_model.create_infer_request()

# load image
img_original = Image.open(IMAGE_PATH)

# preprocess image
img_original = img_original.resize((IMAGE_SIZE, IMAGE_SIZE))
img_original = np.array(img_original, dtype='float32')
img_original = img_original.transpose(2, 0, 1)
img_original = img_original / 255
img_original = img_original.reshape(1, 3, IMAGE_SIZE, IMAGE_SIZE)

# create tensor from external memory
input_tensor = ov.Tensor(array=img_original, shared_memory=False)

# set input tensor for model with one input
infer_request.set_input_tensor(input_tensor)

# start request
infer_request.start_async()
infer_request.wait()

# get output tensor for model with one output
output = infer_request.get_output_tensor()
output_data = output.data

# perform NMS
result_boxes, result_scores, result_class_names = nmr.nms(output_data[0])

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
img_pred.save('result-runtime.png')
