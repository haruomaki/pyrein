import pyrein
import pygame
from pyrein.easing import ease_out
from dataclasses import dataclass


@dataclass
class State:
    x: int
    y: int


Action = int | None


def simulate(state: State, action: Action) -> State:
    if action is None:
        return state
    dx = [0, 0, -1, 1][action]
    dy = [-1, 1, 0, 0][action]
    return State(state.x + dx, state.y + dy)


def render(prev: State, curr: State):
    print(f"[render] 現在の状態は{curr}です。")
    while True:
        # 円を描画
        x = pyrein.lerp(200 + prev.x * 30, 200 + curr.x * 30, ease_out(0.5))
        y = pyrein.lerp(200 + prev.y * 30, 200 + curr.y * 30, ease_out(0.5))
        pygame.draw.circle(pyrein.screen, (23, 200, 100), (x, y), 80)
        yield


def decide():
    action: Action = None
    while pyrein.elapsed < 1:
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


pyrein.run(simulate, decide, render, State(0, 0))
