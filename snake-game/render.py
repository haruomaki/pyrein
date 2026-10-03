# render.py
import pygame
from game import Scene, Rect, Circle, Text

def draw_scene(
    surface: pygame.Surface,
    scene: Scene,
    cell: int,
    font: pygame.font.Font | None = None,
) -> None:
    surface.fill(scene.bg)
    for item in scene.items:
        if isinstance(item, Rect):
            pygame.draw.rect(
                surface, item.color,
                (item.x * cell, item.y * cell, item.w * cell, item.h * cell),
            )
        elif isinstance(item, Circle):
            pygame.draw.circle(
                surface, item.color,
                (int(item.cx * cell), int(item.cy * cell)),
                int(item.r * cell),
            )
        elif isinstance(item, Text):
            if font is None:
                font = pygame.font.SysFont(None, 24)
            img = font.render(item.text, True, item.color)
            surface.blit(img, (item.x * cell, item.y * cell))
