#!/bin/bash

LIVE_NOVEL_ROOT=$(pwd)

cd "$LIVE_NOVEL_ROOT/backend"
# removes blinker, as seems that pip is not able to remove it, and that would prevent the installation of flask

apt-get -y remove python3-blinker
# install requirements
pip install -r requirements.txt

#isntall tensorRT
pip install tensorrt --extra-index-url https://pypi.nvidia.com
# install requirements for torch, because is strange and want them in a particular way
#python -m pip install -r torch_requirements.txt
# install stuff that must be installed later other wise overwritten (maybe)
#python -m pip install -r requirements2.txt

cd "$LIVE_NOVEL_ROOT/backend/models"
# dowloads the llm model to execute
wget -O "model.gguf" [file $MODEL_DOWNLOAD_URL]
