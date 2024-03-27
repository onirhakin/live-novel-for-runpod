#!/bin/bash

LIVE_NOVEL_ROOT=$(pwd)

# dowloads the llm model to execute in subshell
( cd "$LIVE_NOVEL_ROOT/backend/models" && wget -O "model.gguf" [file $MODEL_DOWNLOAD_URL] ) &

# removes blinker, as seems that pip is not able to remove it, and that would prevent the installation of flask
apt-get -y remove python3-blinker

# inatall transformers for tokenizer to measure token length
pip install transformers

# download,compile and install llama-cpp-python with GPU enabled (cuda 11.8)
CUDACXX="/usr/local/cuda-11.8/bin/nvcc" CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=all-major" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade

# install flask for making the server
pip install flask
pip install flask-cors

# wait for the subshell download to finish
wait

echo 'Programs installed and model downloaded.  Environment is ready!'


