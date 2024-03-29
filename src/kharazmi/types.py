from typing import Iterable, Protocol, TypeAlias, runtime_checkable, Union


TypedValue: TypeAlias = Union["SupportsBoolean", "SupportsArithmetic", "SupportsString", "SupportsList"]


class Function(Protocol):
    def __call__(self, *args: "TypedValue") -> "TypedValue": ...


class ListFactory(Protocol):
    def __call__(self, items: Iterable["TypedValue"]) -> "SupportsList": ...


@runtime_checkable
class SupportsBoolean(Protocol):
    """
    As python does not allow us to overload binary operators (AND, OR, NOT)
    We're overloading bitwise binary operators (&, |, ^, ~).
    This way native python boolean objects will supoort this protocol as well.
    And because bitwise operation on boolean value returns the correct result,
    it will work correctly in all cases.
    """

    def __and__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...
    def __rand__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...

    def __or__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...
    def __ror__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...

    def __xor__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...
    def __rxor__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...

    def __invert__(self) -> "SupportsBoolean": ...

    def __eq__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...
    def __ne__(self, other: "SupportsBoolean", /) -> "SupportsBoolean": ...

    def __str__(self) -> "SupportsString": ...


@runtime_checkable
class SupportsConditional(Protocol):
    """
    We need a way to implement conditional expressions on custom data types.
    The way we've chose is for data types to define a _cond__ function which,
    takes two inputs and returns a mix of them based on the conditions its in.

    For example if the class that implements it is a list of boolean, it can
    take two other lists with the same length (of any other types) and return
    a mix of them by applying `x if cond else y` operation elementwise.

    It's upto the implementor to consider all the edge cases and supports elementwise
    operations if they see fit.
    """

    def _cond__(self, choice1: "TypedValue", choice2: "TypedValue") -> "TypedValue": ...


@runtime_checkable
class SupportsArithmetic(Protocol):
    def __abs__(self) -> "SupportsArithmetic": ...

    def __add__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...
    def __radd__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...

    def __sub__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...
    def __rsub__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...

    def __mul__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...
    def __rmul__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...

    def __truediv__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...
    def __rtruediv__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...

    def __neg__(self) -> "SupportsArithmetic": ...
    def __eq__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...
    def __ne__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...

    def __gt__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...
    def __lt__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...
    def __ge__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...
    def __le__(self, other: "SupportsArithmetic") -> "SupportsBoolean": ...

    def __pow__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...
    def __rpow__(self, other: "SupportsArithmetic") -> "SupportsArithmetic": ...

    def __str__(self) -> "SupportsString": ...


@runtime_checkable
class SupportsString(Protocol):
    def __add__(self, other: "SupportsString") -> "SupportsString": ...
    def __len__(self) -> "SupportsArithmetic": ...

    def __eq__(self, other: "SupportsString") -> "SupportsBoolean": ...
    def __ne__(self, other: "SupportsString") -> "SupportsBoolean": ...


@runtime_checkable
class SupportsList(Protocol):
    def __add__(self, other: "SupportsList") -> "SupportsList": ...
    def __len__(self) -> "SupportsArithmetic": ...

    def __contains__(self, other: "TypedValue") -> "SupportsBoolean": ...

    def __eq__(self, other: "SupportsList") -> "SupportsBoolean": ...
    def __ne__(self, other: "SupportsList") -> "SupportsBoolean": ...

    def __str__(self) -> "SupportsString": ...
