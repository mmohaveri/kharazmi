from abc import ABC, abstractmethod
import functools

from typing import Dict, List, Set, Union

from .types import DataContainer, Function


class BaseExpression(ABC):
    @abstractmethod
    def evaluate(self, **kwargs: DataContainer) -> DataContainer:
        raise NotImplementedError

    @property
    @abstractmethod
    def variables(self) -> Set[str]:
        raise NotImplementedError

    def __add__(self, operand: "BaseExpression") -> "BaseExpression":
        return AdditionExpression(self, operand)

    def __radd__(self, operand: "BaseExpression") -> "BaseExpression":
        return AdditionExpression(operand, self)

    def __sub__(self, operand: "BaseExpression") -> "BaseExpression":
        return SubtractionExpression(self, operand)

    def __rsub__(self, operand: "BaseExpression") -> "BaseExpression":
        return SubtractionExpression(operand, self)

    def __mul__(self, operand: "BaseExpression") -> "BaseExpression":
        return MultiplicationExpression(self, operand)

    def __rmul__(self, operand: "BaseExpression") -> "BaseExpression":
        return MultiplicationExpression(operand, self)

    def __truediv__(self, operand: "BaseExpression") -> "BaseExpression":
        return DivisionExpression(self, operand)

    def __rtruediv__(self, operand: "BaseExpression") -> "BaseExpression":
        return DivisionExpression(operand, self)

    def __pow__(self, operand: "BaseExpression") -> "BaseExpression":
        return ExponentiationExpression(self, operand)

    def __rpow__(self, operand: "BaseExpression") -> "BaseExpression":
        return ExponentiationExpression(operand, self)

    def __neg__(self) -> "BaseExpression":
        return NegativeExpression(self)


class BinaryExpression(BaseExpression):
    def __init__(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> None:
        self._right_hand_side = right_hand_side
        self._left_hand_side = left_hand_side

    def evaluate(self, **kwargs: DataContainer) -> DataContainer:
        left_hand_side = self._left_hand_side.evaluate(**kwargs)
        right_hand_side = self._right_hand_side.evaluate(**kwargs)
        return self._apply(left_hand_side, right_hand_side)

    @property
    def variables(self) -> Set[str]:
        return self._right_hand_side.variables.union(self._left_hand_side.variables)

    @property
    @abstractmethod
    def _operator(cls) -> str: ...

    @abstractmethod
    def _apply(self, left_hand_side: DataContainer, right_hand_side: DataContainer) -> DataContainer: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left_hand_side)}, {repr(self._right_hand_side)})"

    def __str__(self) -> str:
        return f"{str(self._left_hand_side)} {self._operator} {str(self._right_hand_side)}"


class UnaryExpression(BaseExpression, ABC):
    def __init__(self, operand: BaseExpression) -> None:
        self._operand = operand

    def evaluate(self, **kwargs: Dict[str, DataContainer]) -> DataContainer:
        value = self._operand.evaluate(**kwargs)
        return self._apply(value)

    @ property
    def variables(self) -> Set[str]:
        return self._operand.variables

    @property
    @abstractmethod
    def _operator(cls) -> str: ...

    @abstractmethod
    def _apply(self, value: DataContainer) -> DataContainer: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._operand)})"

    def __str__(self) -> str:
        return f"{self._operator}{str(self._operand)}"


class Number(BaseExpression):
    def __init__(self, value: str) -> None:
        self._value: DataContainer

        try:
            self._value = int(value)
        except ValueError:
            try:
                self._value = float(value)
            except ValueError:
                self._value = complex(value)

    def evaluate(self, **kwargs: DataContainer) -> DataContainer:
        return self._value

    @ property
    def variables(self) -> Set[str]:
        return set()

    def __repr__(self):
        return f"Number('{repr(self._value)}')"

    def __str__(self):
        return str(self._value)


class Variable(BaseExpression):
    def __init__(self, name: str) -> None:
        self._name = name

    def evaluate(self, **kwargs: DataContainer) -> DataContainer:
        if self._name not in kwargs:
            raise ValueError(f"Variable `{self._name}` does not have a value!")

        return kwargs[self._name]

    @ property
    def variables(self) -> Set[str]:
        return {self._name}

    def __repr__(self) -> str:
        return f"Variable('{self._name}')"

    def __str__(self) -> str:
        return self._name


class FunctionExpression(BaseExpression):
    supported_functions: Dict[str, Function] = {}

    def __init__(self, name: str, argument: "FunctionArgument") -> None:
        self._name = name
        self._argument = argument

    def evaluate(self, **kwargs: DataContainer) -> DataContainer:
        if self._name not in self.supported_functions.keys():
            raise ValueError(f"Function `{self._name}` has not been defined!")

        return self.supported_functions[self._name](*self._argument.evaluate(**kwargs))

    @ property
    def variables(self) -> Set[str]:
        return self._argument.variables

    @ classmethod
    def register(cls, name: str, runner: Function) -> None:
        cls.supported_functions[name] = runner

    def __repr__(self) -> str:
        return f"Function('{self._name}', {repr(self._argument)})"

    def __str__(self) -> str:
        return f"{self._name}({str(self._argument)})"


register_function = FunctionExpression.register


class FunctionArgument(object):
    def __init__(self, *expression: BaseExpression) -> None:
        self._expressions = [*expression]

    def evaluate(self, **kwargs: DataContainer) -> List[DataContainer]:
        return [expression.evaluate(**kwargs) for expression in self._expressions]

    @ property
    def variables(self) -> Set[str]:
        return functools.reduce(lambda a, b: a.union(b), [expression.variables for expression in self._expressions])

    def __add__(self, op: Union[BaseExpression, 'FunctionArgument']) -> 'FunctionArgument':
        if isinstance(op, FunctionArgument) is False and isinstance(op, BaseExpression) is False:
            raise NotImplementedError()

        if isinstance(op, FunctionArgument):
            return FunctionArgument(*self._expressions, *op._expressions)

        return FunctionArgument(*self._expressions, op)

    def __radd__(self, op: Union[BaseExpression, 'FunctionArgument']) -> 'FunctionArgument':
        if isinstance(op, FunctionArgument) is False and isinstance(op, BaseExpression) is False:
            raise NotImplementedError()

        if isinstance(op, FunctionArgument):
            return FunctionArgument(*op._expressions, *self._expressions)

        return FunctionArgument(op, *self._expressions)

    def __repr__(self) -> str:
        return f"FunctionArgument({', '.join([repr(expression) for expression in self._expressions])})"

    def __str__(self) -> str:
        return f"{', '.join([str(expression) for expression in self._expressions])}"


class AdditionExpression(BinaryExpression):
    @property
    def _operator(self) -> str:
        return "+"

    def _apply(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> BaseExpression:
        return left_hand_side + right_hand_side


class SubtractionExpression(BinaryExpression):
    @property
    def _operator(self) -> str:
        return "-"

    def _apply(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> BaseExpression:
        return left_hand_side - right_hand_side


class MultiplicationExpression(BinaryExpression):
    @property
    def _operator(self) -> str:
        return "*"

    def _apply(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> BaseExpression:
        return left_hand_side * right_hand_side


class DivisionExpression(BinaryExpression):
    @property
    def _operator(self) -> str:
        return "/"

    def _apply(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> BaseExpression:
        return left_hand_side / right_hand_side


class ExponentiationExpression(BinaryExpression):
    @property
    def _operator(self) -> str:
        return "^"

    def _apply(self, left_hand_side: BaseExpression, right_hand_side: BaseExpression) -> BaseExpression:
        return left_hand_side ** right_hand_side


class NegativeExpression(UnaryExpression):
    @property
    def _operator(self) -> str:
        return "-"

    def _apply(self, value: BaseExpression) -> BaseExpression:
        return -value
