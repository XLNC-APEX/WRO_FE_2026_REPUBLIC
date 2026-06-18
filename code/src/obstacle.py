#!/usr/bin/env pybricks-micropython
from config import (
    CHECK_DISTANCE,
    OBSTACLE_COUNTER_GYRO_KP,
    OBSTACLE_GYRO_KP,
    OBSTACLE_HIGH_SPEED,
    OBSTACLE_LOW_SPEED,
    START_CHECK_DISTANCE,
    MAX_STEER,
)
from line_detection import LineDetector
from ObstacleDetection import ObstacleDetection
from pixy2 import Pixy2
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port
from pybricks.tools import wait, StopWatch
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
gyro.calibrate() # type: ignore

steering = Steering(motor=steering_motor, gyro=gyro)
line_checker = LineDetector(color_sensor=color_sensor)
wall_distance_keeper = DistanceKeeperOneUltrasonic(ultrasonic)
obstacle_detection = ObstacleDetection(camera)

passed_lines = 0
distance = 0

steering.reset_angles()
rear_motor.reset_angle(0)

ev3.speaker.beep()


direction_set = False
is_turning = False
clockwise = True
wall_correction = 0
pixy_correction = 0


def parking_out():
    dist = ultrasonic.distance()
    print(dist)
    print(dist)
    print(dist)
    if dist > 200:
        print("cw, steer +max")
        clockwise = True
        steering_motor.track_target(-45)
    else:
        print("ccw, steer -max")
        clockwise = False
        steering_motor.track_target(45)
    direction_set = True
    wait(200)
    rear_motor.run(OBSTACLE_HIGH_SPEED)
    timer = StopWatch()
    start = timer.time()
    while timer.time() - start < 800:
        if clockwise:
            steering_motor.track_target(-45)
        else:
            steering_motor.track_target(45)
    print(steering_motor.angle())

    wait(100)


parking_out()

if clockwise:
    Kp = OBSTACLE_GYRO_KP
else:
    Kp = OBSTACLE_COUNTER_GYRO_KP

while passed_lines < 12:
    new_distance = get_distance(rear_motor)
    if abs(new_distance - distance) > CHECK_DISTANCE:
        line = line_checker.check_line()
        is_turning = False

        if line != ColorID.WHITE:
            ev3.speaker.beep()
            is_turning = True
            distance = new_distance
            passed_lines += 1
            if clockwise:
                steering.increase_target_angle(-90)
            else:
                steering.increase_target_angle(90)
            wait(300)

    pixy_correction = obstacle_detection.get_correction()

    if direction_set and not clockwise and pixy_correction == 0:
        wall_correction = wall_distance_keeper.correction(
            clockwise, steering.heading, steering.target_angle
        )
    else:
        wall_correction = 0


    steer = steering.pid(Kp=Kp, pixy=pixy_correction, wall=wall_correction)

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
    
pixy_correction = 0
wall_correction = 0

rear_motor.run(OBSTACLE_LOW_SPEED)
finish_dist = get_distance(rear_motor)
while abs(get_distance(rear_motor) - finish_dist) < 2000:
    wall_correction = wall_distance_keeper.correction(
        clockwise, steering.heading, steering.target_angle
    )
    pixy_correction = obstacle_detection.get_correction()
    steering.pid(Kp=Kp, wall=wall_correction, pixy=pixy_correction)

rear_motor.stop()

ev3.speaker.beep()
ev3.speaker.beep()
ev3.speaker.beep()
