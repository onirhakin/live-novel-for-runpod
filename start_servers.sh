#!/bin/bash

LIVE_NOVEL_ROOT=$(pwd)


# Start the web server
cd "$LIVE_NOVEL_ROOT/frontend"
web_server_command="python -m http.server"
$web_server_command &
echo $! > web_server_pid.txt

cd "$LIVE_NOVEL_ROOT/backend"
# Start the database server
python_server_command="python app.py"
$python_server_command &
echo $! > python_server_pid.txt

echo "Servers started."