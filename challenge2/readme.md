## Challenge 2

To run the OpenVINO serving with the model

```
docker run -v $(pwd)/best_model:/models -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_name challenge2 --model_path /models --layout NCHW:NCHW --port 9000 --rest_port 9001;
```
