import pyrein
import pygame
from pyrein.easing import ease_out
from dataclasses import dataclass

# 色の定義
BACKGROUND = (15, 56, 15)
GRID_COLOR = (20, 80, 20)
SNAKE_HEAD = (23, 200, 100)  # ミントグリーン
SNAKE_BODY = (34, 139, 34)  # フォレストグリーン
FOOD_COLOR = (220, 20, 60)  # クリムゾン
TEXT_COLOR = (255, 255, 255)

GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 10


@dataclass
class State:
    direction: int
    x: int
    y: int


Action = int | None


dt = 0.3


def simulate(state: State, action: Action) -> State:
    BACK = [(0, 1), (1, 0), (2, 3), (3, 2)]
    if action is not None and not (state.direction, action) in BACK:
        state.direction = action
    state.x += [0, 0, -1, 1][state.direction]
    state.y += [-1, 1, 0, 0][state.direction]
    return state


def draw_grid():
    """グリッド線を描画"""
    for w in range(GRID_WIDTH + 1):
        pyrein.draw.line(
            GRID_COLOR,
            (w * GRID_SIZE, 0),
            (w * GRID_SIZE, GRID_HEIGHT * GRID_SIZE),
        )
    for h in range(GRID_HEIGHT + 1):
        pyrein.draw.line(
            GRID_COLOR,
            (0, h * GRID_SIZE),
            (GRID_WIDTH * GRID_SIZE, h * GRID_SIZE),
        )


def render(prev: State, curr: State):
    while True:
        draw_grid()
        # 円を描画
        x = pyrein.lerp(prev.x * GRID_SIZE, curr.x * GRID_SIZE, ease_out(dt, 1.5))
        y = pyrein.lerp(prev.y * GRID_SIZE, curr.y * GRID_SIZE, ease_out(dt, 1.5))
        pyrein.draw.circle(SNAKE_HEAD, (x, y), GRID_SIZE / 2)
        yield


def decide():
    action: Action = None
    while pyrein.elapsed < dt:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = 0
        if keys[pygame.K_DOWN]:
            action = 1
        if keys[pygame.K_LEFT]:
            action = 2
        if keys[pygame.K_RIGHT]:
            action = 3
        yield

    return action


pyrein.run(simulate, decide, render, State(1, 0, 0))
