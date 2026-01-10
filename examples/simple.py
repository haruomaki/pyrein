import pyrein


def simulate(state: int, message: int) -> int:
    return state + message


def render(current: int, next: int, time: float):
    print(f"[render] 現在の状態は{current}です。")


def input_provider() -> int:
    return 5


pyrein.run_game(0, simulate, render, input_provider)
