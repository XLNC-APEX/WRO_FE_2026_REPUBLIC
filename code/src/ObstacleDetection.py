from config import MIN_OBSTACLE_AREA
from pixy2 import Pixy2, Block
from utils import Curve2D, Point2D

CAM_WIDTH = 316
CAM_HEIGHT = 208
Kp = 1.7
# v1
# RED_LINE = Line2D(-1.206, 172.5)
# GREEN_LINE = Line2D(1.747, -364.8)
# GREEN_LINE = Line2D(1.206, -208.596)
# GREEN_LINE = RED_LINE.invert_in_x_range_to(CAM_WIDTH)

# v2
# RED_CURVE = Curve2D(0.003517, -1.282576, 129.94021)

# v3
# RED_CURVE = Curve2D(0.003517, -1.282576, 120)
# GREEN_CURVE = Curve2D(-0.004968, 1.319625, 215.021075)

# v4
# red: y = 124.599494*x^0 + -1.865848*x^1 + 0.007155*x^2
# green: y = 187.050712*x^0 + 1.880561*x^1 + -0.007322*x^2
RED_CURVE = Curve2D(0.007155, -1.865848, 124.599494)
GREEN_CURVE = Curve2D(-0.007322, 1.880561, 187.050712)

def filter(block: Block) -> bool:
    if (block.height * block.width) > MIN_OBSTACLE_AREA:
        if crop_filter(block.x_center, block.y_center):
            return True
    return False


def crop_filter(x: int, y: int) -> bool:
    H_CROP = 10

    V_TOP_CROP = 35
    V_BOTTOM_CROP = 38
    if (x > H_CROP) and (x < (CAM_WIDTH - H_CROP)):
        if y > V_TOP_CROP:
            if y < (CAM_HEIGHT - V_BOTTOM_CROP):
                return True
    return False


class ObstacleDetection:
    def __init__(self, camera: Pixy2):
        self.camera = camera
        self.red_obstacles = []
        self.green_obstacles = []
        self.correction = 0

    def update(self):
        try:
            self.red_obstacles = self.camera.get_blocks(1, 1)
            self.green_obstacles = self.camera.get_blocks(2, 1)
        except Exception as e:
            print(e)

    def _calculate_correction(self, p: Point2D, curve: Curve2D) -> float:
        # Simple x error instead of perpendicular, it is easier to compute and is proportional? to perp.
        return (curve.get_x(p.y) - p.x) * Kp

    def get_correction(self):
        self.update()

        red_count = self.red_obstacles[0]
        green_count = self.green_obstacles[0]

        red_area = 0
        green_area = 0
        self.correction = 0

        if red_count > 0:
            red = self.red_obstacles[1][0]
            red_area = red.height * red.width

        if green_count > 0:
            green = self.green_obstacles[1][0]
            green_area = green.height * green.width

        if (red_count > 0) and (red_area > green_area) and filter(red):
            self.correction = self._calculate_correction(
                Point2D(red.x_center, red.y_center), RED_CURVE
            )
        elif (green_count > 0) and (filter(green)):
            self.correction = self._calculate_correction(
                Point2D(green.x_center, green.y_center), GREEN_CURVE
            )

        print(
            "pixy-correction: ",
            self.correction,
            "green: ",
            green_count,
            "red: ",
            red_count,
        )
        return self.correction
