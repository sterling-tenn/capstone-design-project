import time
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import conf as conf
import threading

class DistSensor:

    def __init__(self, trigger_pin, echo_pin, name="Sensor"):
        self.myfactory = PiGPIOFactory()
        self.sensor = DistanceSensor(trigger=trigger_pin, echo=echo_pin, pin_factory=self.myfactory)
        self.name = name
        self._distance = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._collision_event = threading.Event()
        self._thread = threading.Thread(target=self._read_distances, daemon=True)
        self._thread.start()

    def _read_distances(self):
        # Continuously reads distances from the sensor in a separate thread.
        while not self._stop_event.is_set():
            with self._lock:
                self._distance = self.sensor.distance * 100  # convert to cm
                if self._distance < conf.STOP_DISTANCE:
                    self._collision_event.set()  # Signal that a collision is detected
                else:
                    self._collision_event.clear()  # No collision
            time.sleep(conf.TIME_DELTA)  # Adjust the sleep duration as needed

    def get_distance(self) -> float:
        # Returns the last measured distance from the sensor in centimeters.
        with self._lock:
            return self._distance if self._distance is not None else 0.0

    def collision_detected(self) -> bool:
        # Returns True if a collision is detected.
        return self._collision_event.is_set()

    def close(self) -> None:
        # Stop the distance reading thread and close the sensor to free up resources.
        self._stop_event.set()
        self._thread.join()
        self.sensor.close()

