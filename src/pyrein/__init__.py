def hello():
    print("こんにちは！")


from typing import TypeVar

S = TypeVar("S")  # State
M = TypeVar("M")  # Message / Input

from typing import Callable

SimulateFn = Callable[[S, M], S]
RenderFn = Callable[[S, S, float], None]


def run_game(initial_state: S, simulate: SimulateFn, render: RenderFn, dummy_imput: M):
    current_state = initial_state

    for t in range(10):
        next_state = simulate(current_state, dummy_imput)
        render(current_state, next_state, t)
        current_state = next_state
