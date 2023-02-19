# Challenge 2 - Computer Vision Challenge Track: Target and Eliminate

Welcome to my computer vision submission project! In this repo I used the [YOLOv5 PyTorch](https://github.com/ultralytics/yolov5) project to create the object detection model and [Intel OpenVINO model server](https://github.com/openvinotoolkit/model_server) to create an inference server.

## Creating the Classification Model

The dataset provided in the hackathon page contains two classes (0 = crop, 1 = weed) and it also provides the data with annotations (which turns out to be compatible with YOLOv5 annotation format). The plan is to change the YOLOv5 training code to use the Intel® Optimization for PyTorch and use the resulting model.

For that I firstly run a test by running the training process using a small YOLOv5 model with 20 epoch. The training is performed on Intel Core i5-10400 with NVIDIA RTX 3060.

| Method | Training Time |
|--------|---------------|
| CPU    | 2 hours 22 minutes 8 seconds |
| CPU with Intel Optimization | 2 hours 9 minutes 57 seconds (-8.56%) |
| GPU    | **6 minutes 25 seconds** (-95.48%) |

Based on the preliminary test, while the Intel Optimization for PyTorch does reduce the training time, but it is only about 5%, whereas the GPU could reach up to 95% of speed up for the training process. This is expected as from my own assumption, my Intel Core CPU does not have the capabilities to speed up the training process significantly.

**Small model metrics (all)**

| Method | Precision | Recall | mAP50 | mAP50-95 |
|--------|-----------|--------|-------|----------|
| CPU    | 0.829     | **0.868**  | **0.905** | **0.593**    |
| CPU with Intel Optimization | **0.838** | 0.814    | 0.875 | 0.528 |
| GPU    | 0.809     | **0.868**  | 0.899 | 0.587    |

The results from the preliminary test is also a bit surprising, overall the CPU has a better recall and mAP metrics but the CPU with Intel Optimization and GPU also has a slightly better precision and recall but I think this is just the nature of deep learning models which sometimes produce a slightly different convergence on each run.

Considering the amount of time required to train a single model, I decided to only use Intel OpenVINO inference and not use the Intel oneDAL for training process.

### Running the Training Process

To run the training process, first I have to create a `dataset.yaml` to instruct the YOLOv5 training script where and what are the classes used in the dataset. For more details, consult the YOLOv5 repository on training a custom model.

```yaml
# absolute path to dataset
path: /home/fahmi/hackathon/intel-oneapi-hackathon/dataset/cropweed/dataset 
train: images  # train images (relative to 'path')
val: images  # val images (relative to 'path')
test:  # test images (optional)

# classes
names:
  0: crop
  1: weed
```

After we have the dataset organized, we can download the pretrained weights from YOLOv5 page and then we can start the training process. Because I have about 32 GB of RAM, I can run the training process with batch size of 24 with RAM caching. You can adjust the training parameters to best suit your environment.

```bash
$ git clone --recurse-submodules https://github.com/fahminlb33/intel-oneapi-hackathon

$ cd intel-oneapi-hackathon/challenge2/yolov5

$ pip install -r requirements.txt

$ python train.py --img 640 --epochs 50 --data ../../dataset/cropweed/dataset.yaml --batch 24 --weights ../../dataset/cropweed/yolov5m.pt --cache ram
```

**Final model metrics**

| Precision | Recall | mAP50 | mAP50-95 |
|-----------|--------|-------|----------|
| 0.841     | 0.918  | 0.946 | 0.699    |

Using the medium pretained model with 50 epochs in fact increases the overall model performance metrics. This model will be available as PyTorch checkpoint in the `yolov5/runs` directory.

### Exporting PyTorch to ONNX and OpenVINO

To use the OpenVINO for the inference engine, we need to convert the saved PyTorch checkpoint into OpenVINO model (and optionally we can save it as ONNX too).

To export the model into ONNX and OpenVINO format:

```bash
$ pwd
~/intel-oneapi-hackathon/challenge2/yolov5

$ python export.py --weights ../models/best.pt --include onnx openvino
```

The model will be cased in the same directory as the checkpoint file.

## Running the Inference

You can run the inference using four  different methods,

1. using the `predict_openvino_runtime.py`,
2. using the OpenVINO model serving and `predict_openvino_serving.py`, and
3. using the web app
4. using the custom REST API from the web app

### Using OpenVINO runtime

> Don't forget to check the `MODEL_PATH` and `IMAGE_PATH` on the script file!

```bash
$ pwd
~/intel-oneapi-hackathon/challenge2

$ python predict_openvino_runtime.py
```

The prediction result will be saved as `result-runtime.png` file.

### Using OpenVINO model serving

To use the model serving, you'll need a Docker installation. Make sure you have the model in a directory organized just like what OpenVINO want it. In this case I saved the models in the `best_model` directory.

```bash
$ docker run -v $(pwd)/best_model:/models -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_name challenge2 --model_path /models --layout NCHW:NCHW --port 9000 --rest_port 9001

[2023-02-19 08:22:28.309][1][serving][info][modelinstance.cpp:793] Loaded model challenge2; version: 1; batch size: 1; No of InferRequests: 4
[2023-02-19 08:22:28.309][1][serving][info][modelversionstatus.cpp:109] STATUS CHANGE: Version 1 of model challenge2 status change. New status: ( "state": "AVAILABLE", "error_code": "OK" )
[2023-02-19 08:22:28.309][1][serving][info][model.cpp:88] Updating default version for model: challenge2, from: 0
[2023-02-19 08:22:28.309][1][serving][info][model.cpp:98] Updated default version for model: challenge2, to: 1
[2023-02-19 08:22:28.309][128][modelmanager][info][modelmanager.cpp:900] Started model manager thread
[2023-02-19 08:22:28.309][1][serving][info][servablemanagermodule.cpp:44] ServableManagerModule started
[2023-02-19 08:22:28.309][129][modelmanager][info][modelmanager.cpp:920] Started cleaner thread
[evhttp_server.cc : 251] NET_LOG: Entering the event loop ...
```

After you have a running OpenVINO model serving container instance, you can make a prediction using the REST or gRPC endpoints. The `predict_openvino_serving.py` will use the REST API from model serving to run the prediction. The prediction will be saved as `result-serving.png`.

> Don't forget to check the `IMAGE_PATH` and `VINO_SERVER` in the script file!

```bash
$ python predict_openvino_serving.py
```

### Using the web app

See [Challenge 2 - Web App](./web-app.md)
