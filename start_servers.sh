#!/bin/bash

# exprot parth to tensorRT si it can be used (do wonder if adding it multiple times creates an issue)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/python3.10/dist-packages/tensorrt

LIVE_NOVEL_ROOT=$(pwd)


# Start the web server
cd "$LIVE_NOVEL_ROOT/frontend"
web_server_command="python -m http.server"
$web_server_command &
echo $! > "$LIVE_NOVEL_ROOT/web_server_pid.txt"

cd "$LIVE_NOVEL_ROOT/backend"
# Start the database server
python_server_command="python app.py"
$python_server_command &
echo $! > "$LIVE_NOVEL_ROOT/python_server_pid.txt"

echo "Servers started."