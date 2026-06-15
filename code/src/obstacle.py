#!/usr/bin/env pybricks-micropython
from config import CHECK_DISTANCE, OBSTACLE_HIGH_SPEED, OBSTACLE_LOW_SPEED, START_CHECK_DISTANCE
from line_detection import LineDetector
from ObstacleDetection import ObstacleDetection
from pixy2 import Pixy2
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port
from pybricks.tools import wait
from steering import Steering
from utils import get_distance, ColorID
from wall_avoidance import DistanceKeeperOneUltrasonic

ev3 = EV3Brick()

steering_motor = Motor(Port.D)
rear_motor = Motor(Port.B)

gyro = GyroSensor(Port.S4, direction=Direction.COUNTERCLOCKWISE)
ultrasonic = UltrasonicSensor(Port.S2)
color_sensor = ColorSensor(Port.S3)
camera = Pixy2(port=Port.S1)
gyro.calibrate()

steering = Steering(motor=steering_motor, gyro=gyro)
line_checker = LineDetector(color_sensor=color_sensor)
wall_distance_keeper = DistanceKeeperOneUltrasonic(ultrasonic)
obstacle_detection = ObstacleDetection(camera)

passed_lines = 0
distance = 0

steering.reset_angles()
rear_motor.reset_angle(0)

ev3.speaker.beep()

rear_motor.run(OBSTACLE_HIGH_SPEED)

direction_set = False
is_turning = False
clockwise = True
wall_correction = 0
pixy_correction = 0

while passed_lines < 12:
    new_distance = get_distance(rear_motor)
    if not direction_set or abs(new_distance - distance) > CHECK_DISTANCE:
        line = line_checker.check_line()
        if (line != ColorID.WHITE) and (not direction_set) and (abs(new_distance - distance) > START_CHECK_DISTANCE):
            direction_set = True
            wait(300)
            if line == ColorID.BLUE:
                clockwise = False

        is_turning = False

        if direction_set and clockwise and line == ColorID.ORANGE:
            ev3.speaker.beep()
            steering.increase_target_angle(-90)
            is_turning = True
            distance = new_distance
            passed_lines += 1
        elif direction_set and not clockwise and line == ColorID.BLUE:
            ev3.speaker.beep()
            steering.increase_target_angle(90)
            is_turning = True
            distance = new_distance
            passed_lines += 1

    pixy_correction = obstacle_detection.get_correction()

    if direction_set and not clockwise:
        wall_correction = wall_distance_keeper.correction(
            clockwise, steering.heading, steering.target_angle
        )
    else:
        wall_correction = 0

    steer = steering.pid(pixy=pixy_correction, wall=wall_correction)

    if abs(steer) > 20 or abs(pixy_correction) > 0 and not is_turning:
        rear_motor.run(OBSTACLE_LOW_SPEED)
    else:
        rear_motor.run(OBSTACLE_HIGH_SPEED)

    # print(
    #     "heading:",
    #     steering.heading,
    #     "target:",
    #     steering.target_angle,
    #     "steer:",
    #     steering_motor.angle(),
    #     "rear motor speed:",
    #     rear_motor.speed()
    # )
    # wait(10)
    wait(10)

rear_motor.run(OBSTACLE_LOW_SPEED)
finish_dist = get_distance(rear_motor)
while abs(get_distance(rear_motor) - finish_dist) < 2000:
    correction = wall_distance_keeper.correction(
        clockwise, steering.heading, steering.target_angle
    )
    steering.pid(wall=wall_correction)

rear_motor.stop()

ev3.speaker.beep()
ev3.speaker.beep()
ev3.speaker.beep()
