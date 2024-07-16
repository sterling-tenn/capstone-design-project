#!/bin/bash
# This script copies a file to a remote host and executes a script on the remote host

LOCAL_FILE_PATH="C:\Users\sterl\Desktop\capstone-design-project\raspberrypi\control-machine\test.json" # File to send
REMOTE_USER="raspberrypi"
REMOTE_HOST="192.168.137.239"
REMOTE_DIR="/home/raspberrypi/CargoBuddy" # Working directory to receive file and execute script
REMOTE_SCRIPT="onlaunch.py" # Remote script to execute

copy_file() {
    scp "$LOCAL_FILE_PATH" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
    if [ $? -eq 0 ]; then
        echo "SUCCESS: File copied successfully."
    else
        echo "ERROR: An error occurred while copying the file."
    fi
}

run_script() {
    ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && python3 $REMOTE_SCRIPT"
    if [ $? -eq 0 ]; then
        echo "SUCCESS: Script executed successfully."
    else
        echo "ERROR: An error occurred while executing the script."
    fi
}

echo "Select an option:"
echo "1) Copy the file"
echo "2) Run the script"
echo "3) Copy the file and run the script"
read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        copy_file
        ;;
    2)
        run_script
        ;;
    3)
        copy_file
        run_script
        ;;
    *)
        echo "ERROR: Invalid choice. Please select 1, 2, or 3."
        ;;
esac