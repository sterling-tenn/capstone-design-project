#!/bin/bash
# This script copies files to a remote host

# List of files to send
LOCAL_FILES=(
            # required files for operation
            "../board/conf.py"
            "../board/server.py"
            "../board/generate_floorplans_map.py"
            "../board/gyroscope.py"
            "../board/robot_controller.py"
            "../board/movement.py"
            "../board/distance_sensor.py"
            "../board/mc_localization.py"
            "../board/astar.py"
            "../board/celltype.py"

            # temp for testing
            "../board/path_demo.json"
            "../board/map_demo.json"

            # "../board/auto.py"
            # "../board/manual.py"
            # "../board/path.json"
            # "../board/ir.py"
            # "../board/servo.py"
            # "../board/ultrasonic.py"
            )

REMOTE_USER="raspberrypi"
REMOTE_HOST="192.168.216.60"
REMOTE_DIR="/home/raspberrypi/CargoBuddy" # Working directory to receive files

for FILE in "${LOCAL_FILES[@]}"; do
    scp "$FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
    if [ $? -eq 0 ]; then
        echo "SUCCESS: File $FILE copied successfully."
    else
        echo "ERROR: An error occurred while copying the file $FILE."
    fi
done
