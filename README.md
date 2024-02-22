This repo is meant to easily load LiveNovel on a Runpod pod.


In the template: 
git clone https://github.com/onirhakin/live-novel-for-runpod.git live-novel
cd live-novel
chmod +x prepare_environment.sh
chmod +x start_servers.sh
chmod +x stop_servers.sh

./prepare_environment.sh
./start_servers.sh


Enviromental variables

MODEL_DOWNLOAD_URL https://huggingface.co/TheBloke/Yarn-Mistral-7B-128k-GGUF/resolve/main/yarn-mistral-7b-128k.Q4_K_M.gguf?download=true


port to listen 8000
