#!/usr/bin/env bash

# Get absolute path to script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Download the model
wget -O $SCRIPT_DIR/models/best.onnx https://blob.kodesiana.com/kodesiana-ai-public/models/intel_oneapi_hackathon_2022/best.onnx
wget -O $SCRIPT_DIR/models/1/best.bin https://blob.kodesiana.com/kodesiana-ai-public/models/intel_oneapi_hackathon_2022/best.bin
