import math
from typing import Callable, Dict, SupportsAbs, SupportsFloat, SupportsRound

from .types import DataContainer, Function, SupportsTrunc

from .models import FunctionExpression


def _abs(inp: DataContainer) -> DataContainer:
    if not isinstance(inp, SupportsAbs):
        raise TypeError("Invalid input type, input does not support `__abs__`.")

    return abs(inp)


def _round(inp: DataContainer) -> DataContainer:
    if not isinstance(inp, SupportsRound):
        raise TypeError("Invalid input type, input does not support `__round__`.")

    return round(inp)


def _trunc(inp: DataContainer) -> DataContainer:
    if not isinstance(inp, SupportsTrunc):
        raise TypeError("Invalid input type, input does not support `__trunc__`.")

    return math.trunc(inp)


def _float_function(func: Callable[[SupportsFloat], float]) -> Callable[[DataContainer], DataContainer]:
    def fn(inp: DataContainer) -> DataContainer:
        if not isinstance(inp, SupportsFloat):
            raise TypeError("Invalid input type, input does not support `float`.")

        return func(inp)

    return fn


def _two_float_function(func: Callable[[SupportsFloat, SupportsFloat], float]) -> Callable[[DataContainer, DataContainer], DataContainer]:
    def fn(inp1: DataContainer, inp2: DataContainer) -> DataContainer:
        if not isinstance(inp1, SupportsFloat):
            raise TypeError("Invalid input type, input does not support `float`.")

        if not isinstance(inp2, SupportsFloat):
            raise TypeError("Invalid input type, input does not support `float`.")

        return func(inp1, inp2)

    return fn


functions: Dict[str, Function] = {
    "abs": _abs,

    "round": _round,
    'floor': _float_function(math.floor),
    'ceil': _float_function(math.ceil),
    'trunc': _trunc,

    "cos": _float_function(math.cos),
    "acos": _float_function(math.acos),
    "cosh": _float_function(math.cosh),
    "acosh": _float_function(math.acosh),
    "sin": _float_function(math.sin),
    'asin': _float_function(math.asin),
    "sinh": _float_function(math.sinh),
    "asinh": _float_function(math.asinh),
    "tan": _float_function(math.tan),
    "atan": _float_function(math.atan),
    "atan2": _two_float_function(math.atan2),
    "tanh": _float_function(math.tanh),
    "atanh": _float_function(math.atanh),
    'copysign': _two_float_function(math.copysign),
    'degrees': _float_function(math.degrees),
    'radians': _float_function(math.radians),

    'erf': _float_function(math.erf),
    'erfc': _float_function(math.erfc),
    'exp': _float_function(math.exp),
    'expm1': _float_function(math.expm1),
    'fabs': _float_function(math.fabs),
    'fmod': _two_float_function(math.fmod),
    'gamma': _float_function(math.gamma),
    'isfinite': _float_function(math.isfinite),
    'isinf': _float_function(math.isinf),
    'isnan': _float_function(math.isnan),
    'lgamma': _float_function(math.lgamma),
    'pow': _two_float_function(math.pow),
    'log': _float_function(math.log),
    'log1p': _float_function(math.log1p),
    'log10': _float_function(math.log10),
    'log2': _float_function(math.log2),
    'remainder': _two_float_function(math.remainder),
    'sqrt': _float_function(math.sqrt),
}


# TODO: Find a way to support variadic functions (min, max, math.fsum, math.gcd, math.hypot)
def activate_builtin_math():
    for name, fn in functions.items():
        FunctionExpression.register(name, fn)
