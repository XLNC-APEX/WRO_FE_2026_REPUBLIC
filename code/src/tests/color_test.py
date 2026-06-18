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
ev3 = EV3Brick()

color_sensor = ColorSensor(Port.S3)

# ORANGE = (28, 12, 9)
# WHITE = (30, 30, 77)
# BLUE = (7, 10, 20)


def recognize_color(rgb: tuple[int, int, int]):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]


    if sum(rgb) >= 125:
        return "ColorID.WHITE"
    elif b * 0.5 > min(r, g):
        return "ColorID.BLUE"
    else:
        return "ColorID.ORANGE"
# (24, 37, 50) blue
# (31, 37, 45) orange

# (15, 25, 31)
while True:
    color = color_sensor.rgb()
    print(color, recognize_color(color))
    wait(50)
