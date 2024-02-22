#!/bin/bash

LIVE_NOVEL_ROOT=$(pwd)

cd "LIVE_NOVEL_ROOT/backend"
# removes blinker, as seems that pip is not able to remove it, and that would prevent the installation of flask
apt-get -y remove python3-blinker
# install requirements
python -m "pip install -r requirements.txt"
# install requirements for torch, because is strange and want them in a particular way
python -m "pip install -r torch_requirements.txt"


# dowloads the llm model to execute
wget -P "$LIVE_NOVEL_ROOT/backend/models" -O "model.gguf" [file $MODEL_DOWNLOAD_URL]
