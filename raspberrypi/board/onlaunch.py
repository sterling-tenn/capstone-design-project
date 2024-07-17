import datetime

# Define the path to the log file
log_file_path = "/home/raspberrypi/CargoBuddy/log.txt"

# Get the current datetime
current_datetime = datetime.datetime.now()

# Append the current datetime to the log file
with open(log_file_path, "a") as log_file:
    log_file.write(f"{current_datetime}\n")

print("Current datetime appended to log.txt")

