#!/bin/bash

LIVE_NOVEL_ROOT=$(pwd)
# Read the web server PID from the file
web_server_pid=$(<"$LIVE_NOVEL_ROOT/web_server_pid.txt")

# Read the database server PID from the file
python_server_pid=$(<"$LIVE_NOVEL_ROOT/python_server_pid.txt")

# Stop the web server
echo "Stopping the web server..."
kill -9 $web_server_pid

# Stop the database server
echo "Stopping the python server..."
kill -9 $python_server_pid

echo "Servers stopped."