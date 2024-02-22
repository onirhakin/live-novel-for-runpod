#!/bin/bash

# Start the web server
web_server_command="python -m http.server"
$web_server_command &
echo $! > web_server_pid.txt

# Start the database server
python_server_command="python app.py"
$python_server_command &
echo $! > python_server_pid.txt

echo "Servers started."