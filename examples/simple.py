import pyrein


def simulate(state: int, input: int) -> int:
    return state + input


def render(prev: int, curr: int, dt: float):
    print(f"[render] 現在の状態は{curr}です。")


def input_provider() -> int:
    return 5


pyrein.run_game(0, simulate, render, input_provider)
