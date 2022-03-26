from typing import Union, Protocol


class SupportMath(Protocol):
    def __add__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __radd__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __sub__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __rsub__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __mul__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __rmul__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __truediv__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __rtruediv__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __pow__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __rpow__(self, operand: "DataContainer") -> "DataContainer":
        raise NotImplementedError

    def __neg__(self) -> "DataContainer":
        raise NotImplementedError


DataContainer = Union[int, float, complex, str, SupportMath]
