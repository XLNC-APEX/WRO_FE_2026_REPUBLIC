import math

from pybricks.ev3devices import Motor

from config import WHEEL_DIAMETER


def constrain(x, low, high):
    return max(low, min(high, x))


def normalize_angle(angle):
    angle %= 360
    if angle >= 180:
        angle -= 360
    if angle < -180:
        angle += 360
    return angle


def get_distance(motor: Motor):
    return motor.angle() / 360 * (WHEEL_DIAMETER * math.pi)


class Line2D:
    def __init__(self, k: float, b: float) -> None:
        self.k: float = k
        self.b: float = b

    def y(self, x: float) -> float:
        return x * self.k + self.b

    def x(self, y: float) -> float:
        return (y - self.b) / self.k

    def invert_in_x_range_to(self, x: float) -> Line2D:
        return Line2D(-self.k, self.b + self.k * x)

    def __str__(self) -> str:
        return f"y = {float(self.k)}x + {float(self.b)}"


class Curve2D:
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c

    def get_x(self, y: float) -> float:
        return self.a * (y**2) + self.b * y + self.c


# RED: y = 129.94021*x^0 + -1.282576*x^1 + 0.003517*x^2
# GREEN: y = 215.021075*x^0 + 1.319625*x^1 + -0.004968*x^2


class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y


def find_perpendicular(heading: int, dist: int, target: int):
    return math.cos((target - heading) * math.pi / 180) * dist


class ColorHSV:
    def __init__(self, h: float, s: float, v: float) -> None:
        self.h: float = h
        self.s: float = s
        self.v: float = v

    def from_rgb(self, rgb: tuple[int, int, int]) -> ColorHSV:
        INV_255 = 1 / 255
        r, g, b = (val * INV_255 for val in rgb)
        cmax, cmax_i = max((val, idx) for idx, val in enumerate(rgb))
        cmin = min(rgb)
        diff = (cmax - cmin) * INV_255
        cmaxf = cmax * INV_255

        h = 0.0
        if cmax != cmin:
            if cmax_i == 0:
                h = (60.0 * ((g - b) / diff) + 360.0) % 360.0
            if cmax_i == 1:
                h = (60.0 * ((b - r) / diff) + 120.0) % 360.0
            if cmax_i == 2:
                h = (60.0 * ((r - g) / diff) + 240.0) % 360.0
        s = 0.0
        if cmax != 0:
            s = (diff / cmaxf) * 100

        v = cmaxf * 100.0

        return ColorHSV(h, s, v)
    
    # def scale_rgb(self, rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    #     rgb[0] *= 2.55
    #     rgb[1] *= 2.55
    #     rgb[2] *= 2.55
    #     return rgb

    def __str__(self) -> str:
        return f"h: {float(self.h)} s: {float(self.s)} v: {float(self.v)}"

    def in_range(self, color: ColorHSV, hp: float, sp: float, vp: float) -> bool:
        if not within_threshold(self.h, color.h, hp):
            return False
        if not within_threshold(self.v, color.v, vp):
            return False
        if not within_threshold(self.s, color.s, sp):
            return False

        return True


def within_threshold(s: float, v: float, th: float) -> bool:
    if ((s + th) > v) and (v > (s - th)):
        return True
    return False


def within_percent(self: float, v: float, p: float) -> bool:
    diff = abs(self - v)
    max_diff = abs(self * (p / 100))
    return diff <= max_diff


class ColorID:
    WHITE = 0
    ORANGE = 1
    BLUE = 2


def clr_print(color: int) -> str:
    if color == ColorID.WHITE:
        return "White"
    elif color == ColorID.ORANGE:
        return "Orange"
    else:
        return "Blue"


def color_dist_squared(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> int:
    return (
        (c2[0] - c1[0]) * (c2[0] - c1[0])
        + (c2[1] - c1[1]) * (c2[1] - c1[1])
        + (c2[2] - c1[2]) * (c2[2] - c1[2])
    )