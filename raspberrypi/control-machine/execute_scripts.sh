# #!/bin/bash
# # This script executes a list of python scripts on the remote host

# # List of remote scripts to execute
# REMOTE_SCRIPTS=("onlaunch.py"
#                 "auto.py") # auto.py is temp for testing, later this will probably be the startup script, and manual.py will be controlled via ssh terminal

# REMOTE_USER="raspberrypi"
# REMOTE_HOST="192.168.1.107"
# REMOTE_DIR="/home/raspberrypi/CargoBuddy" # Working directory where scripts are located

# # environtment and install dependencies
# ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && python3 -m venv env && ./env/bin/pip install -r requirements.txt"

# for SCRIPT in "${REMOTE_SCRIPTS[@]}"; do
#     ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && ./env/bin/python3 $SCRIPT" # run in virtual environment
#     if [ $? -eq 0 ]; then
#         echo "SUCCESS: Script $SCRIPT executed successfully."
#     else
#         echo "ERROR: An error occurred while executing the script $SCRIPT."
#     fi
# done