import pyrein
import pygame
from pygame import Vector2 as Vec2
from pyrein.easing import ease_out
from dataclasses import dataclass
from random import choice

# 色の定義
BACKGROUND = (15, 56, 15)
GRID_COLOR = (20, 80, 20)
SNAKE_HEAD = (23, 200, 100)  # ミントグリーン
SNAKE_BODY = (34, 139, 34)  # フォレストグリーン
FOOD_COLOR = (220, 20, 60)  # クリムゾン
TEXT_COLOR = (255, 255, 255)

GRID_SIZE = 30
GRID_WIDTH = 6
GRID_HEIGHT = 6


@dataclass
class State:
    direction: int
    body: list[Vec2]
    apple: Vec2


Action = int | None


dt = 0.3
pyrein.draw.camera.set_offset(
    (GRID_WIDTH - 1) / 2 * GRID_SIZE, (GRID_HEIGHT - 1) / 2 * GRID_SIZE
)
DIRECTIONS = [Vec2(0, -1), Vec2(0, 1), Vec2(-1, 0), Vec2(1, 0)]


def initialize() -> State:
    return State(1, [Vec2(0, 0)], Vec2(5, 5))


def simulate(state: State, action: Action) -> State:
    BACK = [(0, 1), (1, 0), (2, 3), (3, 2)]
    if action is not None and not (state.direction, action) in BACK:
        state.direction = action
    new_head = state.body[0] + DIRECTIONS[state.direction]

    # ゲームオーバー判定
    if (
        new_head.x < 0
        or GRID_WIDTH <= new_head.x
        or new_head.y < 0
        or GRID_HEIGHT <= new_head.y
        or new_head in state.body
    ):
        print("ゲームオーバー！")
        state.body = [Vec2(GRID_WIDTH // 3, GRID_HEIGHT // 2)]
        return state

    if state.body[0] == state.apple:
        # しっぽはそのままに頭が長くなる
        state.body = [new_head] + state.body

        # 新しいリンゴが出現
        cand: set[tuple[float, float]] = set()
        for w in range(GRID_WIDTH):
            for h in range(GRID_HEIGHT):
                cand.add((w, h))
        for b in state.body:
            cand.remove((b.x, b.y))

        apple = choice(list(cand))
        # print(apple)
        state.apple = Vec2(apple)
    else:
        # しっぽが消えて頭が長くなる
        state.body = [new_head] + state.body[0:-1]
        print(state.body[0], state.apple)

    return state


def draw_grid():
    """グリッド線を描画"""
    for w in range(GRID_WIDTH):
        pyrein.draw.line(
            GRID_COLOR,
            (w * GRID_SIZE, 0),
            (w * GRID_SIZE, (GRID_HEIGHT - 1) * GRID_SIZE),
        )
    for h in range(GRID_HEIGHT):
        pyrein.draw.line(
            GRID_COLOR,
            (0, h * GRID_SIZE),
            ((GRID_WIDTH - 1) * GRID_SIZE, h * GRID_SIZE),
        )


def render(prev: State, curr: State):
    while True:
        draw_grid()

        # リンゴを描画
        pyrein.draw.circle(FOOD_COLOR, curr.apple * GRID_SIZE, GRID_SIZE / 3)

        # 円を描画
        if len(prev.body) != len(curr.body):
            prev.body = [prev.body[0]] + prev.body
        for i in range(len(curr.body)):
            pr = prev.body[i]
            cr = curr.body[i]
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


pyrein.run(
    simulate,
    decide,
    render,
    initialize,
)
