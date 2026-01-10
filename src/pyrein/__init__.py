from typing import TypeVar, Callable

S = TypeVar("S")  # State
M = TypeVar("M")  # Message / Input


Simulator = Callable[[S, M], S]
Renderer = Callable[[S, S, float], None]
InputProvider = Callable[[], M]


def run_game(
    initial_state: S,
    simulate: Simulator[S, M],
    render: Renderer[S],
    input_provider: InputProvider[M],
) -> None:
    state = initial_state

    for t in range(10):
        msg = input_provider()
        next_state = simulate(state, msg)
        render(state, next_state, float(t))
        state = next_state
