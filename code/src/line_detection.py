from pybricks.ev3devices import ColorSensor, UltrasonicSensor
from utils import ColorID, ColorHSV

COLOR_ORANGE = ColorHSV(15, 75, 12)  # CMYK (0, 60, 100, 0)
COLOR_BLUE = ColorHSV(235, 84, 4.8)  # CMYK(100, 80, 0, 0)
# COLOR_WHITE = ColorHSV(222, 52, 25)


class LineDetector:
    def __init__(self, color_sensor: ColorSensor):
        self.color_sensor = color_sensor

    def recognize_color(self, rgb: tuple[int, int, int]) -> int:
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        
        # 31 15 14 orange
        # TODO: fix color detection (saturation)
        if sum(rgb) >= 125:
            return ColorID.WHITE
        elif b >= min(r, g):
            return ColorID.BLUE
        else:
            return ColorID.ORANGE


        # if sum(rgb) >= 100:
        #     return ColorID.WHITE
        # elif b >= min(r, g):
        #     return ColorID.BLUE
        # else:
        #     return ColorID.ORANGE

    # def recognize_color(self, rgb: tuple[int, int, int]) -> int:
    #     color = ColorHSV.from_rgb(rgb)
    #     # if color.in_range(COLOR_ORANGE, 20, 15, 10):
    #     #     return ColorID.ORANGE
    #     # if color.in_range(COLOR_BLUE, 10, 10, 5):
    #     #     return ColorID.BLUE
    #     # return ColorID.WHITE
    #     # if color.s < 60:
    #     #     return ColorID.WHITE
    #     # elif color.h > 200:
    #     #     return ColorID.BLUE
    #     # return ColorID.ORANGE
    #     if color.in_range(COLOR_ORANGE, 20, 15, 10):
    #         return ColorID.ORANGE
    #     if (color.s < 60) or (color.v > 21):
    #         return ColorID.WHITE
    #     return ColorID.BLUE

    def check_line(self):
        color = self.color_sensor.rgb()
        # print("rgb: ", color)
        return self.recognize_color(color)


# class LineDetectorObstacle:
#     # def __init__(self, ultrasonic_left: UltrasonicSensor, ultrasonic_right: UltrasonicSensor) -> None:
#     #     self.ultrasonic_left = ultrasonic_left
#     #     self.ultrasonic_right = ultrasonic_right

# TRIGGER_DISTANCE = 1500
    
# def check_line_obstacle(dist_left, dist_right):
#     if dist_left > TRIGGER_DISTANCE or dist_right > TRIGGER_DISTANCE:
#         return True
    