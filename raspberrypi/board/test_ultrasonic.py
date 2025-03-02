from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(trigger=23, echo=24) # physical pins 16, 18

try:
    while True:
        distance = sensor.distance * 100  # convert to cm
        print(f"Distance: {distance:.2f} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Program interrupted by user. Exiting...")

sensor.close()