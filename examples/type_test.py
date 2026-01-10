from typing import Callable


def call_func[T, R](f: Callable[[T], R], arg: T) -> R:
    return f(arg)


def f(xs: list[int]) -> int:
    return len(xs)


res = call_func(f, [34])
print(res)
