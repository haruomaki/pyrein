import pyrein


def simulate(state: int, input: int) -> int:
    return state + input


def render(prev: int, curr: int, dt: float):
    print(f"[render] 現在の状態は{prev}です。")


def input_provider() -> int:
    return 5


env = pyrein.Env[int, int]()
env.simulate = simulate
env.render = render
env.input_provider = input_provider
env.run_game(0)
