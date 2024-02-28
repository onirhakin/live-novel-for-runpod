This repo is meant to easily load LiveNovel on a Runpod pod.

To run in the shell for installation and run:
git clone https://github.com/onirhakin/live-novel-for-runpod.git live-novel
cd live-novel
chmod +x prepare_environment.sh
chmod +x start_servers.sh
chmod +x stop_servers.sh

./prepare_environment.sh
./start_servers.sh


Enviromental variables


MODEL_DOWNLOAD_URL https://huggingface.co/TheBloke/Yarn-Mistral-7B-64k-GGUF/resolve/main/yarn-mistral-7b-64k.Q5_K_M.gguf?download=true



port to listen 8000, 6969
