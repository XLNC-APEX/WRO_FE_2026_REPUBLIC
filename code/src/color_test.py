#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from line_detection import LineDetector, match_vector_color

# from pybricks.media.ev3dev import SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait
from utils import clr_print, color_dist_squared

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)

# ORANGE = (28, 12, 9)
# WHITE = (30, 30, 77)
# BLUE = (7, 10, 20)

line_detector = LineDetector(color_sensor=color_sensor)


# def recognize_color(rgb: tuple[int, int, int]):
#     r = rgb[0]
#     g = rgb[1]
#     b = rgb[2]


#     if sum(rgb) >= 125:
#         return "white"
#     elif b >= max(r, g):
#         return "blue"
#     else:
#         return "orange"


# ORANGE_COLOR = (31, 15, 14)
ORANGE_COLOR = (30, 11, 3)
# BLUE_COLOR = (10, 16, 27)
BLUE_COLOR = (0, 1, 5)

while True:
    color = color_sensor.rgb()
    print(
        color,
        clr_print(line_detector.recognize_color(color)),
        clr_print(match_vector_color(color)),
        color_dist_squared(ORANGE_COLOR, color),
        color_dist_squared(BLUE_COLOR, color)
    )
    wait(50)
