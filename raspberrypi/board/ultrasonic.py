from gpiozero import DistanceSensor
from time import sleep

uds = DistanceSensor(trigger=27, echo=17)
while True:
	print(uds.distance)
	sleep(1)