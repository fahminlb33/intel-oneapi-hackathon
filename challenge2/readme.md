# Challenge 2 - Computer Vision Challenge Track: Target and Eliminate

Class:

* 0 = crop
* 1 = weed

To run the training process

```bash
python train.py --img 640 --epochs 20 --data ../dataset/cropweed/dataset.yaml --batch 24 --device cpu --weights ../dataset/cropweed/yolov5s.pt --cache ram
```

To export the model into ONNX and OpenVINO

```bash
python export.py --weights ../challenge2/models/ipex/best_ipex.pt --include onnx openvino
```

To run the OpenVINO serving with the model

```bash
docker run -v $(pwd)/best_model:/models -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_name challenge2 --model_path /models --layout NCHW:NCHW --port 9000 --rest_port 9001;
```


https://intel.github.io/intel-extension-for-pytorch/xpu/latest/tutorials/examples.html
