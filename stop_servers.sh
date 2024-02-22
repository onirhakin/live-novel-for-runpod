#!/bin/bash

# Read the web server PID from the file
web_server_pid=$(<web_server_pid.txt)

# Read the database server PID from the file
python_server_pid=$(<python_server_pid.txt)

# Stop the web server
echo "Stopping the web server..."
kill $web_server_pid

# Stop the database server
echo "Stopping the python server..."
kill $python_server_pid

echo "Servers stopped."