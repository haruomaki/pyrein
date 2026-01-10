from typing import TypeVar, Callable

S = TypeVar("S")  # State
M = TypeVar("M")  # Message / Input

Simulator = Callable[[S, M], S]
Renderer = Callable[[S, S, float], None]
InputProvider = Callable[[], M]


class Env[S, M]:
    simulate: Simulator[S, M]
    render: Renderer[S]
    input_provider: InputProvider[M]

    def run_game(
        self,
        initial_state: S,
    ) -> None:
        state = initial_state

        for t in range(10):
            msg = self.input_provider()
            next_state = self.simulate(state, msg)
            self.render(state, next_state, float(t))
            state = next_state
