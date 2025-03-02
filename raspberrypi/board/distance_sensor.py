from gpiozero import DistanceSensor
import conf as conf

class DistSensor:

    def __init__(self, trigger_pin, echo_pin, id):
        self.sensor = DistanceSensor(trigger=trigger_pin, echo=echo_pin)
        self.id = id
        self._distance = 0.0
        self._collision_event = False

    def get_distance(self) -> float:
        # Returns the last measured distance from the sensor in centimeters.
        self._distance = self.sensor.distance * 100 
        return self._distance

    def is_collision_detected(self) -> bool:
        # Returns True if a collision is detected.
        return self._collision_event

    def set_collision(self):
        # Returns True if a collision is detected.
        self._collision_event = True

    def unset_collision(self):
        # Returns True if a collision is detected.
        self._collision_event = False

    def get_id(self) -> int:
        return self.id

if __name__ == "__main__":
    import os
    import time as t

    center = DistSensor(conf.TRIGGER_PIN_CENTRE, conf.ECHO_PIN_CENTRE, conf.CENTOR_SENSOR_ID)
    left = DistSensor(conf.TRIGGER_PIN_LEFT, conf.ECHO_PIN_LEFT, conf.LEFT_SENSOR_ID)
    right = DistSensor(conf.TRIGGER_PIN_RIGHT, conf.ECHO_PIN_RIGHT, conf.RIGHT_SENSOR_ID)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=================================================")
        print(f"ID: {left.get_id()} | Dist: {left.get_distance()}")
        print(f"ID: {center.get_id()} | Dist: {center.get_distance()}")
        print(f"ID: {right.get_id()} | Dist: {right.get_distance()}")
        print("=================================================")
        t.sleep(0.1)
