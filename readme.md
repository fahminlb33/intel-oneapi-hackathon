To use Intel oneDNN
TF_ENABLE_ONEDNN_OPTS=1 

------------------ dataset cropweed

0 crop
1 weed

satu row dari txt
1 0.503906 0.416992 0.691406 0.685547
[class] (x1, y1) (x2, y2)

----------

python train.py --img 640 --epochs 20 --data ../dataset/cropweed/dataset.yaml --batch 24 --device cpu --weights ../dataset/cropweed/yolov5s.pt --cache ram


python export.py --weights ../challenge2/models/ipex/best_ipex.pt --include onnx openvino

