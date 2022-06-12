from typing import NoReturn, Optional
from sly import Parser  # pyright: ignore[reportMissingTypeStubs]

from .exceptions import ParseError
from .models import BaseExpression, FunctionExpression, Number, Variable, FunctionArgument
from .lexer import EquationLexer


class EquationParser(Parser):
    """
    EquationParser implements a CFG parser for the following grammar:

    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression POWER expression
               | ( expression )
               | MINUS expression
               | NUMBER
               | IDENTIFIER
               | IDENTIFIER ( argument )

    argument   : expression
               | argument , expression
    """

    def __init__(self):
        self.lexer = EquationLexer()

    def parse(self, inp: str) -> Optional[BaseExpression]:
        return super().parse(self.lexer.tokenize(inp))

    tokens = EquationLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),  # type: ignore
        ("left", TIMES, DIVIDE),  # type: ignore
        ("left", POWER),  # type: ignore
        ('right', UMINUS),  # type: ignore
    )

    start = 'expression'

    @_("expression PLUS expression")  # type: ignore
    def expression(self, p) -> BaseExpression:
        return p.expression0 + p.expression1

    @_("expression MINUS expression")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return p.expression0 - p.expression1

    @_("expression TIMES expression")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return p.expression0 * p.expression1

    @_("expression DIVIDE expression")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return p.expression0 / p.expression1

    @_("expression POWER expression")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return p.expression0 ** p.expression1

    @_("'(' expression ')'")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return p.expression

    @_("MINUS expression %prec UMINUS")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return -p.expression

    @_("NUMBER")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return Number(p[0])

    @_("IDENTIFIER")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return Variable(p[0])

    @_("IDENTIFIER '(' argument ')'")  # type: ignore
    def expression(self, p) -> BaseExpression:  # type: ignore
        return FunctionExpression(p[0], p[2])

    @_("expression")  # type: ignore
    def argument(self, p) -> FunctionArgument:  # type: ignore
        return FunctionArgument(p.expression)

    @_("argument ',' expression")  # type: ignore
    def argument(self, p) -> FunctionArgument:  # type: ignore
        return p.argument + p.expression

    def error(self, p) -> NoReturn:
        if p is None:
            raise ParseError(f"Incomplete expression.")

        raise ParseError(f"Invalid expression. Error occurred in position {p.index}")
