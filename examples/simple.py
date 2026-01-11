import pyrein
import pygame


def simulate(state: int, input: int) -> int:
    print(f"[simulate] {state=}")
    return state + input


def hokan(t: float) -> float:
    if t > 0.5:
        return 1
    return 1 - 4 * (t - 0.5) ** 2


def render(prev: int, curr: int):
    # print(f"[render] 現在の状態は{prev}です。")
    while True:
        t = pyrein.elapsed
        # 円を描画
        x = (200 + prev * 10) * (1 - hokan(t)) + (200 + curr * 10) * hokan(t)
        pygame.draw.circle(pyrein.screen, (23, 200, 100), (x, 200), 80)
        yield


def input_provider() -> int:
    return 5


pyrein.run(simulate, render, input_provider, 0)
