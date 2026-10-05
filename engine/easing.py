from typing import Callable


def clamp(start: float = 0, end: float = 1) -> Callable[[float], float]:
    def inner(x: float) -> float:
        return min(max(x, start), end)

    return inner


def ease_out(duration: float, power: float = 2) -> Callable[[float], float]:
    def inner(x: float) -> float:
        x = clamp(0, duration)(x)
        return 1 - ((duration - x) / duration) ** power

    return inner
