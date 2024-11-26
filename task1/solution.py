from typing import Any


def strict(func):
    def wrapper(*args: Any, **kwargs: dict[Any: Any]) -> Any:
        annotations = func.__annotations__
        for arg_name, arg in zip(annotations.keys(), args):
            expected_type = annotations.get(arg_name)
            if not isinstance(arg, expected_type):
                raise TypeError(f"Argument '{arg_name}' must be {expected_type}, got {type(arg)}")
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


answer = sum_two(12, 13)
print(answer)
