import pygame
import pyrein
from typing import Tuple, Sequence, Union

# 型エイリアスを定義
ColorValue = Union[
    pygame.Color, Tuple[int, int, int], Tuple[int, int, int, int], int, str
]
Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]


def line(
    color: ColorValue,
    start_pos: Coordinate,
    end_pos: Coordinate,
    width: int = 1,
) -> pygame.Rect:
    return pygame.draw.line(pyrein.screen, color, start_pos, end_pos, width)


def circle(
    color: ColorValue,
    center: Coordinate,
    radius: float,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> pygame.Rect:
    return pygame.draw.circle(
        pyrein.screen,
        color,
        center,
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )
