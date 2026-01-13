from typing import Callable


def clamp(start: float = 0, end: float = 1) -> Callable[[float], float]:
    def inner(x: float) -> float:
        return min(max(x, start), end)

    return inner


def ease_out(length: float, power: float = 2) -> Callable[[float], float]:
    def inner(x: float) -> float:
        x = clamp(0, length)(x)
        return 1 - ((length - x) / length) ** power

    return inner
