# from utils import color_dist_squared
from config import BLUE_COLOR, ORANGE_COLOR, MIN_COLOR_DIST_SQUARED


class ColorID:
    WHITE = 0
    ORANGE = 1
    BLUE = 2


def color_dist_squared(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> int:
    return (
        (c2[0] - c1[0]) * (c2[0] - c1[0])
        + (c2[1] - c1[1]) * (c2[1] - c1[1])
        + (c2[2] - c1[2]) * (c2[2] - c1[2])
    )


def match_vector_color(rgb: tuple[int, int, int]) -> int:
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


def clr_print(color: int) -> str:
    if color == ColorID.WHITE:
        return "White"
    elif color == ColorID.ORANGE:
        return "Orange"
    else:
        return "Blue"


def test_color(clr: tuple[int, int, int]):
    db = color_dist_squared(ORANGE_COLOR, clr)
    do = color_dist_squared(BLUE_COLOR, clr)
    
    print(db, do, clr_print(match_vector_color(clr)))

test_color((34, 13, 16))
test_color((9, 17, 23))
test_color((24, 37, 50))
test_color((31, 37, 45))
