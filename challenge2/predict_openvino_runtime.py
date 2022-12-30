import time
import cv2
from PIL import Image
import numpy as np
import openvino.runtime as ov

core = ov.Core()

compiled_model = core.compile_model("best2.onnx", "AUTO")
infer_request = compiled_model.create_infer_request()

# im = Image.open("../dataset/cropweed/data/agri_0_3.jpeg")
# im = im.resize((640, 640))
# pix = np.array(im, dtype=np.float32)
# pix = pix.transpose(2, 0, 1)
# pix = pix.reshape(1, 3, 640, 640)

im = cv2.imread("../dataset/cropweed/data/agri_0_14.jpeg")
im = cv2.resize(im, (640, 640))
pix = np.array(im, dtype=np.float32) / 255
pix = pix.transpose(2, 0, 1)
pix = np.expand_dims(pix, axis=0)

# Create tensor from external memory
input_tensor = ov.Tensor(array=pix, shared_memory=False)

# Set input tensor for model with one input
infer_request.set_input_tensor(input_tensor)

infer_request.start_async()
infer_request.wait()

# Get output tensor for model with one output
output = infer_request.get_output_tensor()
output_data = output.data

import challenge2.web_app.nmr as nmr

result_boxes, result_scores, result_class_names = nmr.nms(output_data[0])

print("TOTAL: ", len(result_boxes))
for i in range(len(result_boxes)):
    print("Bounding box: ", result_boxes[i])
    print("Scores: ", result_scores[i])
    print("Classes: ", result_class_names[i])

# ----- DRAW

image = Image.open("../dataset/cropweed/data/agri_0_14.jpeg")
original_size = image.size[:2]

img = np.asarray(image)

result_boxes = nmr.scale_coords((640,640), np.array(result_boxes), (original_size[1],original_size[0]))
font = cv2.FONT_HERSHEY_SIMPLEX 

# org 
org = (20, 40) 
    
# fontScale 
fontScale = 0.5
    
# Blue color in BGR 
color = (255, 255, 0) 
    
# Line thickness of 1 px 
thickness = 1

for i,r in enumerate(result_boxes):

    org = (int(r[0]),int(r[1]))
    cv2.rectangle(img, (int(r[0]),int(r[1])), (int(r[2]),int(r[3])), (255,0,0), 1)
    cv2.putText(img, str(int(100*result_scores[i])) + '%  ' + str(result_class_names[i]), org, font,  
                fontScale, color, thickness, cv2.LINE_AA)

save_result_filepath = "test.jpg"
cv2.imwrite(save_result_filepath,img[:,:,::-1])
