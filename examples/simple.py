import pyrein
import pygame
from pyrein.easing import ease_out


def simulate(state: int, msg: int) -> int:
    # print(f"[simulate] {state=}")
    return state + msg


def render(prev: int, curr: int):
    print(f"[render] 現在の状態は{curr}です。")
    while True:
        # 円を描画
        x = pyrein.lerp(200 + prev * 10, 200 + curr * 10, ease_out(0.5))
        pygame.draw.circle(pyrein.screen, (23, 200, 100), (x, 200), 80)
        yield


def decide():
    while pyrein.elapsed < 1:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print("<-")
        if keys[pygame.K_RIGHT]:
            print("->")
        yield

    return 10


pyrein.run(simulate, decide, render, 0)
