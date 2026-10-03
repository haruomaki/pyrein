# game.py
from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import IntEnum
from typing import NamedTuple
import random

# ============ Scene（描画プリミティブ） ============
@dataclass
class Rect:
    x: float; y: float; w: float; h: float
    color: tuple[int, int, int]

@dataclass
class Circle:
    cx: float; cy: float; r: float
    color: tuple[int, int, int]

@dataclass
class Text:
    x: float; y: float
    text: str
    color: tuple[int, int, int]

@dataclass
class Scene:
    items: list[Rect | Circle | Text] = field(default_factory=list)
    bg: tuple[int, int, int] = (20, 20, 30)

# ============ ゲームの型 ============
class Action(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @property
    def delta(self) -> tuple[int, int]:
        return {
            Action.UP:    (0, -1),
            Action.DOWN:  (0,  1),
            Action.LEFT:  (-1, 0),
            Action.RIGHT: ( 1, 0),
        }[self]

    @property
    def opposite(self) -> "Action":
        return {
            Action.UP: Action.DOWN,
            Action.DOWN: Action.UP,
            Action.LEFT: Action.RIGHT,
            Action.RIGHT: Action.LEFT,
        }[self]

@dataclass
class State:
    snake: list[tuple[int, int]]      # 先頭が頭
    direction: Action
    food: tuple[int, int]
    grid: tuple[int, int]
    alive: bool
    score: int
    rng: random.Random

class StepResult(NamedTuple):
    state: State
    reward: float
    terminated: bool
    truncated: bool
    info: dict

# ============ 遷移 ============
def initial_state(
    grid: tuple[int, int] = (10, 10),
    rng: random.Random | None = None,
) -> State:
    if rng is None:
        rng = random.Random()
    w, h = grid
    cx, cy = w // 2, h // 2
    snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
    food = _spawn_food(snake, grid, rng)
    return State(snake, Action.RIGHT, food, grid, True, 0, rng)

def _spawn_food(snake, grid, rng) -> tuple[int, int]:
    w, h = grid
    free = [(x, y) for x in range(w) for y in range(h) if (x, y) not in snake]
    if not free:
        return (-1, -1)
    return rng.choice(free)

def step(state: State, action: Action) -> StepResult:
    # ゲームオーバー後は何もしない
    if not state.alive:
        return StepResult(state, 0.0, True, False, {})

    # 逆方向は無視（その場で向き維持）
    if action == state.direction.opposite:
        action = state.direction

    dx, dy = action.delta
    hx, hy = state.snake[0]
    nx, ny = hx + dx, hy + dy
    w, h = state.grid

    # 壁衝突
    if not (0 <= nx < w and 0 <= ny < h):
        dead = replace(state, alive=False, direction=action)
        return StepResult(dead, -1.0, True, False, {"reason": "wall"})

    # 自分の体に衝突（尻尾は今回動くので除外しない、簡易版）
    if (nx, ny) in state.snake[:-1]:
        dead = replace(state, alive=False, direction=action)
        return StepResult(dead, -1.0, True, False, {"reason": "self"})

    new_head = (nx, ny)
    ate = (nx, ny) == state.food

    if ate:
        new_snake = [new_head] + state.snake
        new_food = _spawn_food(new_snake, state.grid, state.rng)
        reward = 1.0
        score = state.score + 1
    else:
        new_snake = [new_head] + state.snake[:-1]
        new_food = state.food
        reward = 0.0
        score = state.score

    new_state = replace(
        state,
        snake=new_snake,
        direction=action,
        food=new_food,
        score=score,
    )
    return StepResult(new_state, reward, False, False, {"ate": ate})

# ============ 描画（Scene構築のみ） ============
COLOR_BG     = (20, 20, 30)
COLOR_SNAKE  = (80, 220, 120)
COLOR_HEAD   = (180, 255, 180)
COLOR_FOOD   = (240, 80, 100)
COLOR_GRID   = (35, 35, 50)

def view(state: State) -> Scene:
    scene = Scene(bg=COLOR_BG)

    # グリッド線（薄く）
    w, h = state.grid
    for x in range(w + 1):
        scene.items.append(Rect(x - 0.02, 0, 0.04, h, COLOR_GRID))
    for y in range(h + 1):
        scene.items.append(Rect(0, y - 0.02, w, 0.04, COLOR_GRID))

    # 餌
    fx, fy = state.food
    if fx >= 0:
        scene.items.append(Rect(fx + 0.15, fy + 0.15, 0.7, 0.7, COLOR_FOOD))

    # 蛇
    for i, (x, y) in enumerate(state.snake):
        color = COLOR_HEAD if i == 0 else COLOR_SNAKE
        scene.items.append(Rect(x + 0.08, y + 0.08, 0.84, 0.84, color))

    return scene
