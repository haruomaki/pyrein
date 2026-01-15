import pygame
import pyrein
from typing import Tuple, Sequence, Union, Any

# 型エイリアスを定義
ColorValue = Union[
    pygame.Color, Tuple[int, int, int], Tuple[int, int, int, int], int, str
]
Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]


class Camera:
    def __init__(self, screen_size: Tuple[int, int] = (800, 600)):
        self.offset = pygame.Vector2(0, 0)
        self.zoom = 1.0
        self.anchor = pygame.Vector2(0.5, 0.5)  # デフォルトで中央
        self.screen_size = pygame.Vector2(screen_size)

    def apply(self, world_pos: Any) -> pygame.Vector2:  # type: ignore
        """ワールド座標 → スクリーン座標"""
        # 1. カメラオフセットを適用
        world_pos: pygame.Vector2 = pygame.Vector2(world_pos)
        result = (world_pos - self.offset) * self.zoom

        # 2. アンカーポイントの適用
        anchor_offset = pygame.Vector2(
            self.screen_size.x * self.anchor.x, self.screen_size.y * self.anchor.y
        )
        result += anchor_offset

        return result

    def set_offset(self, x: float, y: float):
        """オフセット設定"""
        self.offset = pygame.Vector2(x, y)

    def set_anchor(self, x: float, y: float):
        """アンカー設定: (0,0)=左上, (0.5,0.5)=中央, (1,1)=右下"""
        self.anchor = pygame.Vector2(x, y)


camera = Camera(screen_size=(800, 600))
camera.set_anchor(0.5, 0.5)  # 画面中央を原点に
camera.offset = pygame.Vector2(0, 0)  # カメラ位置


def line(
    color: ColorValue,
    start_pos: Coordinate,
    end_pos: Coordinate,
    width: int = 1,
) -> pygame.Rect:
    return pygame.draw.line(
        pyrein.screen, color, camera.apply(start_pos), camera.apply(end_pos), width
    )


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
        camera.apply(center),
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )
