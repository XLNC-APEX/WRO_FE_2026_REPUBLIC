from pybricks.ev3devices import ColorSensor, UltrasonicSensor

from config import BLUE_COLOR, MIN_COLOR_DIST_SQUARED, N_CONSEQ_COLORS, ORANGE_COLOR
from utils import ColorHSV, ColorID, color_dist_squared

COLOR_ORANGE = ColorHSV(15, 75, 12)  # CMYK (0, 60, 100, 0)
COLOR_BLUE = ColorHSV(235, 84, 4.8)  # CMYK(100, 80, 0, 0)
# COLOR_WHITE = ColorHSV(222, 52, 25)


class LineDetector:
    def __init__(self, color_sensor: ColorSensor):
        self.color_sensor = color_sensor
        # self.blue_cnt: int = 0
        # self.oran_cnt: int = 0
        self.non_white_cnt: int = 0

    def recognize_color(self, rgb: tuple[int, int, int]) -> int:
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        # 31 15 14 orange
        # TODO: fix color detection (saturation)
        if sum(rgb) >= 120:
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

    def is_line_white(self) -> bool:
        rgb = self.color_sensor.rgb()
        r, g, b = rgb
        # print(rgb)

        if sum(rgb) < 50:
            return False

        if b > r:
            return True
        else:
            return False

    def check_line(self):
        color = self.color_sensor.rgb()
        print("rgb: ", color)
        return self.recognize_color(color)

    def is_line_white_filtered(self) -> bool:
        if not self.is_line_white():
            self.non_white_cnt += 1
            if self.non_white_cnt >= N_CONSEQ_COLORS:
                return False
        else:
            self.non_white_cnt = 0
        return True
    
    def is_white_v(self) -> bool:
        rgb = self.color_sensor.rgb()
        clr = self.match_vector_color(rgb)
        return clr == ColorID.WHITE
        

    def match_vector_color(self, rgb: tuple[int, int, int]) -> int:
        blue_dist = color_dist_squared(BLUE_COLOR, rgb)
        oran_dist = color_dist_squared(ORANGE_COLOR, rgb)
        if blue_dist < MIN_COLOR_DIST_SQUARED:
            if oran_dist < blue_dist:
                return ColorID.ORANGE
            return ColorID.BLUE
        if oran_dist < MIN_COLOR_DIST_SQUARED:
            if blue_dist < oran_dist:
                return ColorID.BLUE
            return ColorID.ORANGE
        return ColorID.WHITE

    # def filter_color(self, color: int) -> int:
    #     if color == ColorID.BLUE:
    #         self.oran_cnt = 0
    #         self.blue_cnt += 1
    #         if self.blue_cnt >= N_CONSEQ_COLORS:
    #             return ColorID.BLUE
    #     elif color == ColorID.ORANGE:
    #         self.blue_cnt = 0
    #         self.oran_cnt += 1
    #         if self.oran_cnt >= N_CONSEQ_COLORS:
    #             return ColorID.ORANGE
    #     else:  # WHITE
    #         self.oran_cnt = 0
    #         self.blue_cnt = 0
    #     return ColorID.WHITE

    # def check_line_filtered(self):
    # color = self.color_sensor.rgb()
    # print("rgb: ", color)
    # return self.filter_color(self.recognize_color(color))


# class LineDetectorObstacle:
#     # def __init__(self, ultrasonic_left: UltrasonicSensor, ultrasonic_right: UltrasonicSensor) -> None:
#     #     self.ultrasonic_left = ultrasonic_left
#     #     self.ultrasonic_right = ultrasonic_right

# TRIGGER_DISTANCE = 1500

# def check_line_obstacle(dist_left, dist_right):
#     if dist_left > TRIGGER_DISTANCE or dist_right > TRIGGER_DISTANCE:
#         return True
