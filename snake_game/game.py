"""
snake_game/game.py
"""

from pygame import Vector2 as Vec2
from dataclasses import dataclass
from random import choice

GRID_SIZE = 40
GRID_WIDTH = 8
GRID_HEIGHT = 8


@dataclass
class State:
    direction: int
    body: list[Vec2]
    apple: Vec2 | None


Action = int | None


DIRECTIONS = [Vec2(0, -1), Vec2(0, 1), Vec2(-1, 0), Vec2(1, 0)]
BACK = [1, 0, 3, 2]  # 方向0の背後は方向1、など


def initialize() -> State:
    return State(1, [Vec2(0, 0)], Vec2(3, 3))


def simulate(state: State, action: Action) -> bool:
    if action is not None and action != BACK[state.direction]:
        state.direction = action
    new_head = state.body[0] + DIRECTIONS[state.direction]

    # ゲームオーバー判定
    if (
        new_head.x < 0
        or GRID_WIDTH <= new_head.x
        or new_head.y < 0
        or GRID_HEIGHT <= new_head.y
        or new_head in state.body[:-1]
    ):
        # print("ゲームオーバー！", len(state.body))
        return False

    # 移動先がエサであれば
    if new_head == state.apple:
        # しっぽはそのままに頭が長くなる
        state.body = [new_head] + state.body

        # 新しいリンゴが出現
        cand: set[tuple[float, float]] = set()
        for w in range(GRID_WIDTH):
            for h in range(GRID_HEIGHT):
                cand.add((w, h))
        for b in state.body:
            cand.remove((b.x, b.y))

        # print("リンゴを食べました。")
        if len(cand) == 0:
            state.apple = None
        else:
            apple = choice(list(cand))
            state.apple = Vec2(apple)
    else:
        # しっぽが消えて頭が長くなる
        state.body = [new_head] + state.body[0:-1]
        # print(state.body[0], state.apple)

    return True
