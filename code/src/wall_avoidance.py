from utils import find_perpendicular
from config import OBS_ULTRASONIC_KP, OPEN_SAFE_DISTANCE_FROM_WALLS, OBSTACLE_SAFE_DISTANCE_FROM_WALLS
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.tools import StopWatch, wait

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
    def __init__(self, ultrasonic: UltrasonicSensor, us_motor: Motor):
        self.ultrasonic = ultrasonic
        self.us_motor = us_motor
        self.first = True
    
    def reset_angle(self):
        self.us_motor.run_time(-500, 1000)
        wait(1000)
        self.us_motor.reset_angle(-90)
        
    def track(self, clockwise: bool):
        if clockwise:
            self.us_motor.track_target(360)
        else:
            self.us_motor.track_target(-90)
    

    def correction(self, clockwise: bool, heading: int, target: int):
        self.track(clockwise)
        # if self.first:
        #     wait(500)
        #     self.first = False
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

        return OBS_ULTRASONIC_KP * error
