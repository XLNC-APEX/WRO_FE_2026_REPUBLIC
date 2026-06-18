from utils import find_perpendicular
from config import OPEN_SAFE_DISTANCE_FROM_WALLS, OBSTACLE_SAFE_DISTANCE_FROM_WALLS
from pybricks.ev3devices import UltrasonicSensor


class DistanceKeeper:
    Kp = 0.2
    
    def __init__(self, ultrasonic_left: UltrasonicSensor, ultrasonic_right: UltrasonicSensor):
        self.ultrasonic_left = ultrasonic_left
        self.ultrasonic_right = ultrasonic_right
        
    def correction(self, clockwise: bool, heading: int, target: int):
        if clockwise:
            d = self.ultrasonic_left.distance()
        else:
            d = self.ultrasonic_right.distance()
            
        # if abs(target - heading) > 40:
        #     error = 0
        # else:
        d = find_perpendicular(heading, d, target)
        error = OPEN_SAFE_DISTANCE_FROM_WALLS - d
        # print("ultrasonic:", d)

        if clockwise:
            error *= -1

        if abs(error) < 5:
            error = 0

        return DistanceKeeper.Kp * error


class DistanceKeeperOneUltrasonic:
    Kp = 0.8
    
    def __init__(self, ultrasonic: UltrasonicSensor):
        self.ultrasonic = ultrasonic

    def correction(self, clockwise: bool, heading: int, target: int):
        d = self.ultrasonic.distance()
        if abs(target - heading) > 30:
            error = 0
        else:
            d = find_perpendicular(heading, d, target)
            error = OBSTACLE_SAFE_DISTANCE_FROM_WALLS - d

        if clockwise:
            error *= -1

        if abs(error) < 5:
            error = 0

        return DistanceKeeperOneUltrasonic.Kp * error
