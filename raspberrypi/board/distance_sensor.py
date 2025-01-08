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

    def _read_distances(self) -> None:
        # Continuously reads distances from the sensor in a separate thread.
        while not self._collision_event:
            self._distance = self.sensor.distance * 100 
            if self._distance < conf.STOP_DISTANCE:
                self._collision_event = True 
            time.sleep(conf.TIME_DELTA)  

    def get_distance(self) -> float:
        # Returns the last measured distance from the sensor in centimeters.
        return self._distance

    def collision_detected(self) -> bool:
        # Returns True if a collision is detected.
        return self._collision_event

    def stop(self) -> None:
        # Stop the distance reading thread and close the sensor to free up resources.
        self._collision_event = True
        self.sensor.close()

    def start(self) -> None:    
        while not self._collision_event:
            self._read_distances()

    def get_id(self) -> int:
        return self.id
