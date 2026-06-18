#!/usr/bin/env pybricks-micropython
from config import CHECK_DISTANCE, OPEN_HIGH_SPEED, OPEN_LOW_SPEED
from line_detection import LineDetector
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port
from pybricks.tools import wait
from steering import Steering
from utils import get_distance, ColorID
from wall_avoidance import DistanceKeeper

ev3 = EV3Brick()

steering_motor = Motor(Port.D)
rear_motor = Motor(Port.B)

gyro = GyroSensor(Port.S4, direction=Direction.COUNTERCLOCKWISE)
ultrasonic_left = UltrasonicSensor(Port.S1)
ultrasonic_right = UltrasonicSensor(Port.S2)
color_sensor = ColorSensor(Port.S3)
gyro.calibrate() # type: ignore

steering = Steering(motor=steering_motor, gyro=gyro)
line_checker = LineDetector(color_sensor=color_sensor)
wall_distance_keeper = DistanceKeeper(ultrasonic_left, ultrasonic_right)

passed_lines = 0
distance = 0

steering.reset_angles()
rear_motor.reset_angle(0)

ev3.speaker.beep()

rear_motor.run(OPEN_HIGH_SPEED)

direction_set = False
is_turning = False
clockwise = True
correction = 0

while passed_lines < 12:
    new_distance = get_distance(rear_motor)
    if not direction_set or abs(new_distance - distance) > CHECK_DISTANCE:
        line = line_checker.check_line()
        if line != ColorID.WHITE and not direction_set:
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

    if direction_set:
        correction = wall_distance_keeper.correction(
            clockwise, steering.heading, steering.target_angle
        )
    else:
        correction = 0

    steer = steering.pid(wall=correction)

    if abs(steer) > 20:
        rear_motor.run(OPEN_LOW_SPEED)
    else:
        rear_motor.run(OPEN_HIGH_SPEED)

    print(
        "heading:",
        steering.heading,
        "target:",
        steering.target_angle,
        "steer:",
        steering_motor.angle(),
        "color:",
        line,
        "distance:",
        new_distance,
        "Is tunring:",
        is_turning,
        "Speed:",
        rear_motor.speed()
    )
    wait(20)

rear_motor.run(OPEN_LOW_SPEED)
finish_dist = get_distance(rear_motor)
while abs(get_distance(rear_motor) - finish_dist) < 2000:
    correction = wall_distance_keeper.correction(
        clockwise, steering.heading, steering.target_angle
    )
    steering.pid(wall=correction)

rear_motor.stop()

ev3.speaker.beep()
ev3.speaker.beep()
ev3.speaker.beep()
