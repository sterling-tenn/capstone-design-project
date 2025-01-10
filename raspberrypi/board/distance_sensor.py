import time
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import conf as conf

class DistSensor:

    def __init__(self, trigger_pin, echo_pin, id):
        self.myfactory = PiGPIOFactory()
        self.sensor = DistanceSensor(trigger=trigger_pin, echo=echo_pin, pin_factory=self.myfactory)
        self.id = id
        self._distance = 0.0
        self._collision_event = False

    def get_distance(self) -> float:
        # Returns the last measured distance from the sensor in centimeters.
        self._distance = self.sensor.distance * 100 
        return self._distance

    def collision_detected(self) -> bool:
        # Returns True if a collision is detected.
        return self._collision_event

    def get_id(self) -> int:
        return self.id
