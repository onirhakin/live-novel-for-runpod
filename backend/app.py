# AI part +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
lns_version = 2 # version that this program uses to save stories in
tokenizer_repo = os.environ.get('TOKENIZER_REPO', "NousResearch/Yarn-Mistral-7b-64k")
context_length = int(os.environ.get('CONTEXT_LENGTH', "64000"))
last_n_tokens_size = int(os.environ.get('LAST_N_TOKENS_SIZE', "64"))
n_gpu_layers = int(os.environ.get('N_GPU_LAYERS', "-1"))

import json
from llama_cpp import Llama
title= ''
story=[]
summary=[]
backupFilePath = "backup.lns"
model_settings = {
    "last_n_tokens_size": last_n_tokens_size,
    "n_ctx": context_length, # context length
    "n_gpu_layers": n_gpu_layers, # gpu layers (-1 all)
}
inference_settings = {
    "top_k": 40,
    "top_p": 0.95,
    "temperature": 0.8,
    "repeat_penalty": 1.1,
    "seed": -1,
    "max_tokens": 50, # this is not the default value but the value i decided
}

# load the LLM (saved in ./models)

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# print("Loading LLM")
#llm = AutoModelForCausalLM.from_pretrained("./models/yarn-mistral-7b-128k.Q4_K_M.gguf", model_type="mistral", gpu_layers=30, context_length=1000, local_files_only=True)



# reload the model with the new settings increaseContextLength determines if the context length shall be increased or not
def reloadModel():
    # checks if the llm object exist, in case deletes it, so then is reloaded better
    global llm
    try:
        llm
    except NameError:
        print("First LLM")
    else:
        del llm
        print("Deleted previous LLM")
    print("Loading LLM")
    global inference_settings
    llm = Llama(model_path="./models/model.gguf",
                n_gpu_layers = model_settings["n_gpu_layers"],
                n_ctx = model_settings["n_ctx"],
                last_n_tokens_size = model_settings["last_n_tokens_size"])

    
reloadModel()

def updateSettings(receivedSettings):
    global inference_settings
    inference_settings = receivedSettings

# save stry backup
def saveBackup():
    data = {
        "version": 2,
        "title": title,
        "story": story,
        "inference_settings": inference_settings
    }
    with open(backupFilePath, 'w') as file:
        json.dump(data, file, indent=4)

#load story backup
def loadBackup():
    loaded_data = None

    try:
        with open(backupFilePath, 'r') as file:
            loaded_data = json.load(file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    parseDataSwitch(loaded_data)
    
def parseDataSwitch(loaded_data):
    if(loaded_data.get('version', 0)==2):
        parseBackupVersion2(loaded_data)
    else:
        parseBackupVersionDefault(loaded_data)
    
def parseBackupVersionDefault(loaded_data):
    # doesn't set  ssettings
    global title
    global story
    title = loaded_data['title']
    story = loaded_data['story']


def parseBackupVersion2(loaded_data):
    global title
    global story
    global inference_settings
    title = loaded_data['title']
    story = loaded_data['story']
    inference_settings = loaded_data['inference_settings']

# loads the backup of the  story at start
loadBackup()

# Load the tokenizer so to be able to compute the number of tokens
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_repo)
def numberOfTokens(text):
    input_ids = tokenizer.encode(text, return_tensors='pt')
    return input_ids.shape[1]

textStream = ""

def streamInference(input, stopAtEndOfSentence=False):
    print("\inference STARTED\n")
    print("###############################################################\n")
    global textStream
    for item in llm(
        input,
        max_tokens = inference_settings["max_tokens"],
        top_k = inference_settings["top_k"],
        top_p = inference_settings["top_p"],
        repeat_penalty = inference_settings["repeat_penalty"],
        temperature = inference_settings["temperature"],
        echo = True,
        seed = inference_settings["seed"],
    #    stop = stop,
        stream = True
    ):
        text = item['choices'][0]['text']
        yield text
        textStream+=text
        print(text, end="", flush=True)
        if(stopAtEndOfSentence):
            if text in ['.', '!', '?']:
                print("End of sentence! Will it stop?")
                return 
    # for text in llm(input, stream=True):
    #     yield text
    #     textStream+=text
    #     print(text, end="", flush=True)
    #     if(stopAtEndOfSentence):
    #         if text in ['.', '!', '?']:
    #             print("End of sentence! Will it stop?")
    #             return 
            
# function to continue text
def streamContinueText(input):
    global textStream
    textStream=""
    print("before streamInference---------------------------------------------------------------------------------------------------------")
    for text in streamInference(input):
        yield text
    print("before stream finish sentence ---------------------------------------------------------------------------------------------------------")
    for text in streamFinishSentence(input, textStream):
        yield text
    print("after stream finish sentence ---------------------------------------------------------------------------------------------------------")
    
    return 

# finishes the sentence is a recursive function
def streamFinishSentence(context, lastGeneration):
    if(checkIfSentenceTruncated(lastGeneration)):
        for text in streamInference(context + lastGeneration, True):
            yield text
        # avoid recursion if it gets outside of the context it goes berserk.
    return 

def streamNextString():
    ms = mergeStoryStrings()
    for text in streamContinueText(ms):
        yield text
    # probably here i should make sure it finishes with a punctuation
    story.append({
        "author": "AI",
        "tokensNumber": numberOfTokens(textStream),
        "text": textStream
    })
    saveBackup()
    return 

def streamUserInput(input):
    if input!="":
        story.append({
            "author": "User",
            "tokensNumber": numberOfTokens(input),
            "text": input
        })
    saveBackup()
    for text in streamNextString():
        yield text
    return 

# inference
# def inference(input, stopAtEndOfSentence=False):
#     print("\inference STARTED\n")
#     print("###############################################################\n")
#     output=""
#     for text in llm(input, stream=True):
#         output+=text
#         print(text, end="", flush=True)
#         if(stopAtEndOfSentence):
#             if text in ['.', '!', '?']:
#                 print("End of sentence! Will it stop?")
#                 return output
#     print("\n inference DONE\n")
#     print("out inference :"+output)
#     return output

    
# chekcs if the last sentence is finished or truncated
def checkIfSentenceTruncated(string):
    print(  "checkIfSentenceTruncated String: "+string)
    cleanedString = string.rstrip()
    print("cleanedString: "+cleanedString)
    if cleanedString == "":
        return False
    if cleanedString[-1] not in ['.', '!', '?']:
        return True
    return False

# # function to continue text
# def continueText(input):
#     llm.config.max_new_tokens=100
#     # llm.config.context_length=10000 #not really working i should reaload the model
#     # llm.config.temperature=1
    
#     output = inference(input)
#     print("out :"+output)
#     output = finishSentence(input, output)
    
#     return output

# # finishes the sentence is a recursive function
# def finishSentence(context, lastGeneration):
#     if(checkIfSentenceTruncated(lastGeneration)):
#         lastGeneration += inference(context + lastGeneration, True)
#         # avoid recursion if it gets outside of the context it goes berserk.
#         #lastGeneration = finishSentence(context, lastGeneration)
#     return lastGeneration


# gets a single text from story list of strings
def mergeStoryStrings():
    texts = [item["text"] for item in story]
    return ''.join(texts)

# computes the total tokens length  of the story
def getStoryTokenLength():
    num = 0
    for item in story:
        num += item["tokensNumber"] 
    return num

def editEntry(id, newText):
    global story
    story[id]["text"] = newText
    story[id]["tokensNumber"] = numberOfTokens(story[id]["text"])
    saveBackup()


# def nextString():
#     ms = mergeStoryStrings()
#     output = continueText(ms)
#     # probably here i should make sure it finishes with a punctuation
#     story.append({
#         "author": "AI",
#         "tokensNumber": numberOfTokens(output),
#         "text": output
#     })
#     saveBackup()
#     return output

# def userInput(input):
#     if input!="":
#         story.append({
#             "author": "User",
#             "tokensNumber": numberOfTokens(input),
#             "text": input
#         })
#     saveBackup()
#     return nextString()

    

# server part ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from flask import Flask, request, stream_template, Response, stream_with_context
import flask
from flask_cors import CORS

#name of the app instance, can be any name
app = Flask(__name__)
CORS(app) # to allow frontend to communicate

#if the backend is runnign we are able to reach it at this http adress of the host
@app.route("/")
#once we reach this adress it executes this funciton
def hello():
    return "Hello, World!"

@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username": "user4",
                "pets": ["hamster"]
            })
            # return flask.jsonify(data)
            return flask.jsonify(story)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        #message = received_data['data']
        message = userInput(received_data['data'])
        return_data = {
            "status": "success",
            "message": f"received: {message}"
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    
# @app.route('/submitUserText', methods=["POST"])
# def submitUserText():
#     print("submitUserText endpoint reached...")
#     if request.method == "POST":
#         received_data = request.get_json()
#         print(f"received data: {received_data}")
#         #message = received_data['data']
#         generatedResponse = userInput(received_data['data'])
#         return_data = {
#             "status": "success",
#             "generatedResponse": generatedResponse,
#             "storyTokensLength": getStoryTokenLength(),
#             "contextWindowTokenLength": llm.config.context_length
#         }
#         return flask.Response(response=json.dumps(return_data), status=201)
    
# starts the generation of the text and retursn the result in small piecese while it gets generated
@app.route('/streamSubmitUserText', methods=["POST"])
def streamSubmitUserText():
    print("streamSubmitUserText endpoint reached...")
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        return flask.Response(stream_with_context(streamUserInput(received_data['data'])))

@app.route('/getTokensStats', methods=["GET"])
def getTokensStats():
    print("getTokensStats endpoint reached...")
    returnData = {
            "status": "success",
            "story_length": getStoryTokenLength(),
            "context_length": llm.n_ctx()
        }
    return flask.jsonify(returnData)

@app.route('/changeContextSize', methods=["POST"])
def changeContextSize():
    print("changeContextSize endpoint reached...")
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        #message = received_data['data']
        changeContextLength(received_data['new_context_size'])
        return_data = {
            "status": "success",
            "story_length": getStoryTokenLength(),
            "context_length": llm.n_ctx()
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    
@app.route('/submitEdit', methods=["POST"])
def submitEdit():
    print("submitEdit endpoint reached...")
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        #message = received_data['data']
        editEntry(received_data['id'],received_data['text'])
        return_data = {
            "status": "success",
            "story_length": getStoryTokenLength(),
            "context_length": llm.n_ctx()
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    
@app.route('/getFullStory', methods=["GET"])
def getFullStory():
    print("getFullStory endpoint reached...")
    returnData = {
            "status": "success",
            "story": story,
            "inference_settings": inference_settings,
            "story_length": getStoryTokenLength(),
            "context_length": llm.n_ctx()
        }
    return flask.jsonify(returnData)

@app.route('/getStoryFile', methods=["GET"])
def getStoryFile():
    print("getStoryFile endpoint reached...")
    # todo add summary entry probably when you add summarization
    returnData = {
            "version": lns_version,
            "title": title,
            "story": story,
            "inference_settings": inference_settings
        }
    return flask.jsonify(returnData)

@app.route('/setStoryFile', methods=["POST"])
def setStoryFile():
    print("setStoryFile endpoint reached...")
    received_data = request.get_json()
    print(f"received data: {received_data}")
    parseDataSwitch(received_data)
    #message = received_data['data']
    # global title
    # global story
    # title =  received_data['title']
    # story = received_data['story']
    # updateSettings(received_data['inference_settings'])
    return_data = {
        "status": "success"
    }
    return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/clearStory', methods=["GET"])
def clearStory():
    print("clearStory endpoint reached...")
    # todo add summary entry probably when you add summarization
    global title
    global story
    title = ""
    story = []
    returnData = {
        "status": "success"
    }
    return flask.Response(response=json.dumps(returnData), status=201)

@app.route('/setSettings', methods=["POST"])
def setSettings():
    print("setSettings endpoint reached...")
    received_data = request.get_json()
    print(f"received data: {received_data}")
    updateSettings(received_data['inference_settings'])
    
    return_data = {
        "status": "success"
    }
    return flask.Response(response=json.dumps(return_data), status=201)

#default port wuld be 5000 we ovverride it, we shoulduse enviromental variables but we lazy now
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969) # this host is necessary to run in runpod