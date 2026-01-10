from typing import Protocol, TypeVar

S = TypeVar("S")  # State
M = TypeVar("M")  # Message / Input


class Simulator(Protocol[S, M]):
    def __call__(self, state: S, input: M) -> S: ...


class Renderer(Protocol[S]):
    def __call__(self, prev: S, curr: S, dt: float) -> None: ...


class InputProvider(Protocol[M]):
    def __call__(self) -> M: ...


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
