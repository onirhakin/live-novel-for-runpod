# Live Novel (Mixtral) [work in progress!!!!]
<span style="color:red; font-weight: bold">
    This is a stupid code, I made it for me, and is not really supposed to be used by other people, but I write this because in few weeks I will forget how to use it XD
</span>

Live Novel uses an LLM to make a novel-like adventure. Some initial text is provided to the app and then it will generate a continuation of the text. When the user/player want to perform an action, they can provide text on their own fort their character actions and then ask the LLM to continue, generating other characters and environment reactions. Playing the game is similar to writing a novel.

![alt text](<readme images/live novel nominal.png>)

This repo contains files to quickly install and run Live Novel on a Runpod pod.
This has been tested with Mistral-7b-64k, but theoretically any text generative model could be used.

It is faster to clone and run installation scripts every time a new pod is created, rather than creating an image with live novel already installed.

## Table of Contents

- [Features](#features)
- [First Time Installation](#first-time-installation)
- [Every Launch Installation](#every-launch-installation)
- [Usage](#usage)
- [License](#license)

## Features

- LLM to continue user text
- Add user text
- Edit story
- Delete story
- Save story
- Load Story
- Change LLM settings
- Go to most recent part
- Report used and available tokens
- Backup of story in case the app crashes

## First time installation

To launch a pod setup with all the needed for live novel,  a Runpod template like the following can be created:

| Field | Value | Notes |
| -------- | -------- | -------- |
| Template Name | Live Novel | Any name you want to give to the template |
| Template Type | GPU Pod |  |
| Container image | runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04 | Image with pythorch 2.1.0, cuda 11.8, python 3.10 installed. Being from Runpod will load quicker than a custom one.|
| Container Registry Credentials| | None |
| Container Start Command|| None|
| Container Disk | 20 GB ||
| Volume Disk| 20 GB||
| Volume Mounth Path| /workspace ||
| Expose HTTP Ports | 8888,8000,6969| 8888 is used for JupyterLab used to access a shell, 8000 is used for the user to access the app via browser, 6969 is used by the frontend to access the backend |
| Expose TCP Ports| 22, | |

And the following enviromental variable must be added
| Key | Value | Notes |
| -------- | -------- | -------- |
| MODEL_DOWNLOAD_URL | https://huggingface.co/TheBloke/Yarn-Mistral-7B-64k-GGUF/resolve/main/yarn-mistral-7b-64k.Q5_K_M.gguf?download=true | URL to download the desired model, in my case Mistral7b 64k context qantized Q5_K_M | 
| TOKENIZER_REPO | NousResearch/Yarn-Mistral-7b-64k | Adress od hugging face repo of the model, where can be found the tokenizer of the downloaded model. |
| CONTEXT_LENGTH | 64000 | Maximum text length the model can tolerate (in tokens) |
| LAST_N_TOKENS_SIZE | 64 | Maximum number of tokens to keep in the last_n_tokens deque. |
| N_GPU_LAYERS | -1 | Number of layer to load in the GPU (-1 is all of them), if they cannot all fit in the GPU it might crash. But this settings works fine for the described model and setup. |

![alt text](<readme images/runpod template.png>)



## Every Launch Installation

To run the application the template must be deployed in a new pod. For this model I use a RTX 4000 Ada from the Community Cloud. Currently $0.21/hr.

Once the pod has beed deployed must go to Connect and connect to the Jupiter lab Port that should be purple.
![alt text](<readme images/connect to jupyter lab.png>)

There, start a terminal and copy paste the following lines, then enter.

```bash
git clone -b mixtral https://github.com/onirhakin/live-novel-for-runpod.git live-novel
cd live-novel
chmod +x prepare_environment.sh
chmod +x start_servers.sh
chmod +x stop_servers.sh

./prepare_environment.sh
./start_servers.sh
```
It will clone this repo and run installation and launch scripts to download the LLM, install and launch Live Novel. It will take about 5 minutes.

Once the process has finished something like this will be shown in the terminal:

![alt text](<readme images/server started.png>)

Now going back to runpod connect, all the port should be active:

![alt text](<readme images/connect to app.png>)

Click on port 8000 to access Live Novel!

![alt text](<readme images/started live novel.png>)

This is what can be seen at start. 

Rememenbr to stop and terminate the pod when no more needed!

## Usage

When the LLM is not generating, at the end of the text there is a box where the user can add text and submit it. It is invisible but a cursor will appear if clicked on it. (If is too hard to find it, there is a button to add "..." in the box so it can be easily clicked on)

The user written text is colored, while the AI generated text is white.
At the beginning of a story must be added an initial text, generally a synopsis like on novels review websites, so that the LLM understands the context.

The user can ask the AI to generate a couple of sentences by clicking the `Submit User Text` button or by clicking Shift+Enter. When the user wants to add its own actions or steer the text in a certain direction he can click at the end of the last sentence and type its own text, then submit it.

If the generated text is poor or has performed action it shouldn't have, the text can be edited by double clikcing on it.

An icon is shown if there is more text to read below and can be clicked to reach text end.

The story can be completely deleted by clicking on `Clear Story` and confirming.

`Reload full story` reloads the story from backend to UI (used if it seems that something is wrong).

The current story can be saved and downloaded to PC by clicking on `Save and download the story`.

A story saved in this way, can be loaded from PC by clicking on `Upload prompt or story from file`. 

Some LLM setting can be changed in `Settings`, `Temperature` is particularly relevant, the higher the more 'original' the text ( standard = 0.7-0.8 ).

On the top right corner, the current amount of token used and total amount of allowed token are displayed. If the limit is surpassed the LLM will produce gibberish.

## License

This code is public just for me to easily clone it, can't stop you from cloning and playing it, not really good with licences, so I'll make it simple, any other use is forbidden, anyway is garbage code XD