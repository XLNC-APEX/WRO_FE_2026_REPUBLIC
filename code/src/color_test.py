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

# from pybricks.media.ev3dev import SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait

from line_detection import LineDetector

ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)

# # ORANGE = (28, 12, 9)% (71.4, 30.6, 22.95) 0.68
# # WHITE = (30, 30, 77)% (76.5, 76.5, 196.35) 0.61
# # BLUE = (7, 10, 20)% (17.85, 25.5, 51) 0.65

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
def is_line_white(rgb: tuple[float, float, float]) -> bool:
    r, g, b = rgb
    print(rgb)

    if sum(rgb) < 70:
        # if sum(rgb) < 40:
        return False

    if b > r:
        return True
    else:
        return False


while True:
    # color = color_sensor.rgb()
    # print(color, line_detector.recognize_color(color))
    print(f"is white: {line_detector.is_line_white()}")
    wait(34)
# colors = [(10, 16, 27), (31, 15, 14), (31, 37, 45), (24, 38, 50), (30, 39, 66)]
# colors = [(r * 2.55, g * 2.55, b * 2.55) for r, g, b in colors]

# print([is_line_white(rgb) for rgb in colors])
