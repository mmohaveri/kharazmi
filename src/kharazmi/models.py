import functools

from typing import Union


class BaseExpression(object):
    def __new__(cls, *args, **kwargs):
        if cls is BaseExpression:
            raise TypeError("'BaseExpression' class may not be instantiated directly")
        return object.__new__(cls)

    def evaluate(self, **kwargs):
        raise NotImplementedError

    @property
    def variables(self) -> set:
        raise NotImplementedError

    def __add__(self, operand: "BaseExpression"):
        return AdditionExpression(self, operand)

    def __radd__(self, operand: "BaseExpression"):
        return AdditionExpression(operand, self)

    def __sub__(self, operand: "BaseExpression"):
        return SubtractionExpression(self, operand)

    def __rsub__(self, operand: "BaseExpression"):
        return SubtractionExpression(operand, self)

    def __mul__(self, operand: "BaseExpression"):
        return MultiplicationExpression(self, operand)

    def __rmul__(self, operand: "BaseExpression"):
        return MultiplicationExpression(operand, self)

    def __truediv__(self, operand: "BaseExpression"):
        return DivisionExpression(self, operand)

    def __rtruediv__(self, operand: "BaseExpression"):
        return DivisionExpression(operand, self)

    def __pow__(self, operand: "BaseExpression"):
        return ExponentiationExpression(self, operand)

    def __rpow__(self, operand: "BaseExpression"):
        return ExponentiationExpression(operand, self)

    def __neg__(self):
        return NegativeExpression(self)


class BinaryExpression(BaseExpression):
    _operator: str

    def __new__(cls, *args, **kwargs):
        if cls is BaseExpression:
            raise TypeError("'BinaryExpression' class may not be instantiated directly")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        self._operand1 = operand1
        self._operand2 = operand2

    def evaluate(self, **kwargs):
        if type(self._operand1) in [int, float, complex]:
            left_hand_side = self._operand1
        else:
            left_hand_side = self._operand1.evaluate(**kwargs)

        if type(self._operand2) in [int, float, complex]:
            right_hand_side = self._operand2
        else:
            right_hand_side = self._operand2.evaluate(**kwargs)

        return self._apply(left_hand_side, right_hand_side)

    @property
    def variables(self) -> set:
        return self._operand1.variables.union(self._operand2.variables)

    def _apply(self, left_hand_side, right_hand_side):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._operand1)}, {repr(self._operand2)})"

    def __str__(self) -> str:
        return f"{str(self._operand1)} {self._operator} {str(self._operand2)}"


class UnaryExpression(BaseExpression):
    _operator: str

    def __new__(cls, *args, **kwargs):
        if cls is BaseExpression:
            raise TypeError("'UnaryExpression' class may not be instantiated directly")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, operand: BaseExpression) -> None:
        self._operand = operand

    def evaluate(self, **kwargs):
        if type(self._operand) in [int, float, complex]:
            value = self._operand
        else:
            value = self._operand.evaluate(**kwargs)

        return self._apply(value)

    @property
    def variables(self) -> set:
        return self._operand.variables

    def _apply(self, value):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._operand)})"

    def __str__(self) -> str:
        return f"{self._operator}{str(self._operand)}"


class Number(BaseExpression):
    def __init__(self, value: str) -> None:
        try:
            self._value = int(value)
        except ValueError:
            try:
                self._value = float(value)
            except ValueError:
                self._value = complex(value)

    def evaluate(self, **kwargs):
        return self._value

    @property
    def variables(self) -> set:
        return set()

    def __repr__(self):
        return f"Number('{repr(self._value)}')"

    def __str__(self):
        return str(self._value)


class Variable(BaseExpression):
    def __init__(self, name: str) -> None:
        self._name = name

    def evaluate(self, **kwargs):
        if self._name not in kwargs:
            raise ValueError(f"Variable `{self._name}` does not have a value!")

        return kwargs[self._name]

    @property
    def variables(self) -> set:
        return {self._name}

    def __repr__(self) -> str:
        return f"Variable('{self._name}')"

    def __str__(self) -> str:
        return self._name


class Function(BaseExpression):
    supported_functions = {}

    def __init__(self, name: str, argument: "FunctionArgument") -> None:
        self._name = name
        self._argument = argument

    def evaluate(self, **kwargs):
        if self._name not in Function.supported_functions.keys():
            raise ValueError(f"Function `{self._name}` has not been defined!")

        return Function.supported_functions[self._name](*self._argument.evaluate(**kwargs))

    @property
    def variables(self) -> set:
        return self._argument.variables

    @staticmethod
    def register(name: str, runner: callable):
        Function.supported_functions[name] = runner

    def __repr__(self) -> str:
        return f"Function('{self._name}', {repr(self._argument)})"

    def __str__(self) -> str:
        return f"{self._name}({str(self._argument)})"


register_function = Function.register


class FunctionArgument(object):
    def __init__(self, *expression: BaseExpression) -> None:
        self._expressions = [*expression]

    def evaluate(self, **kwargs):
        return self._map(lambda e: e.evaluate(**kwargs))

    @property
    def variables(self) -> set:
        return functools.reduce(lambda a, b: a.union(b), self._map(lambda e: e.variables))

    def _map(self, fn):
        return [fn(expression) for expression in self._expressions]

    def __add__(self, op: Union[BaseExpression, 'FunctionArgument']) -> 'FunctionArgument':
        if type(op) != FunctionArgument and isinstance(op, BaseExpression) is False:
            raise NotImplementedError()

        if type(op) == FunctionArgument:
            return FunctionArgument(*self._expressions, *op._expressions)

        return FunctionArgument(*self._expressions, op)

    def __radd__(self, op: Union[BaseExpression, 'FunctionArgument']) -> 'FunctionArgument':
        if type(op) not in [BaseExpression, FunctionArgument]:
            raise NotImplementedError()

        if type(op) == FunctionArgument:
            return FunctionArgument(*op._expressions, *self._expressions)

        return FunctionArgument(op, *self._expressions)

    def __repr__(self) -> str:
        return f"FunctionArgument({', '.join(self._map(repr))})"

    def __str__(self) -> str:
        return f"{', '.join(self._map(str))}"


class AdditionExpression(BinaryExpression):
    _operator = "+"

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        super().__init__(operand1, operand2)

    def _apply(self, left_hand_side, right_hand_side):
        return left_hand_side + right_hand_side


class SubtractionExpression(BinaryExpression):
    _operator = "-"

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        super().__init__(operand1, operand2)

    def _apply(self, left_hand_side, right_hand_side):
        return left_hand_side - right_hand_side


class MultiplicationExpression(BinaryExpression):
    _operator = "*"

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        super().__init__(operand1, operand2)

    def _apply(self, left_hand_side, right_hand_side):
        return left_hand_side * right_hand_side


class DivisionExpression(BinaryExpression):
    _operator = "/"

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        super().__init__(operand1, operand2)

    def _apply(self, left_hand_side, right_hand_side):
        return left_hand_side / right_hand_side


class ExponentiationExpression(BinaryExpression):
    _operator = "^"

    def __init__(self, operand1: BaseExpression, operand2: BaseExpression) -> None:
        super().__init__(operand1, operand2)

    def _apply(self, left_hand_side, right_hand_side):
        return left_hand_side ** right_hand_side


class NegativeExpression(UnaryExpression):
    _operator = "-"

    def __init__(self, operand: BaseExpression) -> None:
        super().__init__(operand)

    def _apply(self, value):
        return -value
