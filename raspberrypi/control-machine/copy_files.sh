#!/bin/bash
# This script copies files to a remote host

# List of files to send
# servo.py, ultrasonic.py, gyroscope.py are temp for testing
LOCAL_FILES=(
            "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/conf.py"
            "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/auto.py"
            "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/manual.py"
            "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/path.json"

            "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/gyroscope.py"
            # "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/servo.py"
            # "C:/Users/sterl/Desktop/capstone-design-project/raspberrypi/board/ultrasonic.py"
            )

REMOTE_USER="raspberrypi"
REMOTE_HOST="192.168.137.176"
REMOTE_DIR="/home/raspberrypi/CargoBuddy" # Working directory to receive files

for FILE in "${LOCAL_FILES[@]}"; do
    scp "$FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
    if [ $? -eq 0 ]; then
        echo "SUCCESS: File $FILE copied successfully."
    else
        echo "ERROR: An error occurred while copying the file $FILE."
    fi
done
