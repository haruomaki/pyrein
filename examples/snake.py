import pyrein
import pygame
from pygame import Vector2 as Vec2
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
    xs: list[int]
    ys: list[int]


Action = int | None


dt = 0.3
pyrein.draw.camera.set_offset(GRID_WIDTH / 2 * GRID_SIZE, GRID_HEIGHT / 2 * GRID_SIZE)


def simulate(state: State, action: Action) -> State:
    BACK = [(0, 1), (1, 0), (2, 3), (3, 2)]
    if action is not None and not (state.direction, action) in BACK:
        state.direction = action
    new_x = state.xs[0] + [0, 0, -1, 1][state.direction]
    new_y = state.ys[0] + [-1, 1, 0, 0][state.direction]
    state.xs = [new_x] + state.xs[0:-1]
    state.ys = [new_y] + state.ys[0:-1]
    print(state.xs)
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
        for i in range(len(curr.xs)):
            pr = Vec2(prev.xs[i], prev.ys[i])
            cr = Vec2(curr.xs[i], curr.ys[i])
            x = pyrein.lerp(pr.x * GRID_SIZE, cr.x * GRID_SIZE, ease_out(dt, 1.5))
            y = pyrein.lerp(pr.y * GRID_SIZE, cr.y * GRID_SIZE, ease_out(dt, 1.5))
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


pyrein.run(simulate, decide, render, State(1, [0, 1, 2, 3, 4], [0, 0, 0, 0, 0]))
