from typing import NoReturn, Optional
from sly import Parser

from .exceptions import ParseError
from .models import BaseExpression, Text, Boolean, Variable, Number, IfExpression, FunctionExpression, FunctionArgument
from .lexer import EquationLexer


class EquationParser(Parser):
    """
    EquationParser implements a CFG parser for the following grammar:

    expression    : expression + expression
                  | expression - expression
                  | expression * expression
                  | expression / expression
                  | expression ^ expression
                  | expression && expression
                  | expression || expression
                  | expression == expression
                  | expression != expression
                  | expression < expression
                  | expression <= expression
                  | expression > expression
                  | expression >= expression
                  | IF expression THEN expression ELSE expression.
                  | - expression
                  | ! expression
                  | ( expression )
                  | function_call
                  | variable
                  | TEXT
                  | NUMBER
                  | TRUE
                  | FALSE

    function_call : IDENTIFIER ( argument )

    variable      : IDENTIFIER

    argument      : expression
                  | argument , expression
    """

    def __init__(self):
        self.lexer = EquationLexer()

    def parse(self, inp: str) -> Optional[BaseExpression]:
        tokens = [t for t in self.lexer.tokenize(inp)]
        print(tokens)
        return super().parse(iter(tokens))

    tokens = EquationLexer.tokens

    precedence = (
        ("left", PLUS, MINUS, OR),
        ("left", TIMES, DIVIDE, AND),
        ("left", POWER),
        ('right', NOT),
        ('left', EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL),
        ('right', UMINUS),
    )

    start = 'expression'

    @_("expression PLUS expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 + p.expression1

    @_("expression MINUS expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 - p.expression1

    @_("expression TIMES expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 * p.expression1

    @_("expression DIVIDE expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 / p.expression1

    @_("expression POWER expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 ** p.expression1

    @_("expression AND expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 & p.expression1

    @_("expression OR expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 | p.expression1

    @_("expression EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 == p.expression1

    @_("expression NOT_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 != p.expression1

    @_("expression GREATER_THAN expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 > p.expression1

    @_("expression GREATER_THAN_OR_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 >= p.expression1

    @_("expression LESS_THAN expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 < p.expression1

    @_("expression LESS_THAN_OR_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 <= p.expression1

    @_("IF expression THEN expression ELSE expression '.'")
    def expression(self, p) -> BaseExpression:
        return IfExpression(p.expression0, p.expression1, p.expression2)

    @ _("MINUS expression %prec UMINUS")
    def expression(self, p) -> BaseExpression:
        return -p.expression

    @ _("NOT expression")
    def expression(self, p) -> BaseExpression:
        return ~p.expression

    @_("'(' expression ')'")
    def expression(self, p) -> BaseExpression:
        return p.expression

    @_("function_call")
    def expression(self, p) -> BaseExpression:
        return p.function_call

    @_("variable")
    def expression(self, p) -> BaseExpression:
        return p.variable

    @ _("TEXT")
    def expression(self, p) -> BaseExpression:
        return Text(p.TEXT)

    @ _("NUMBER")
    def expression(self, p) -> BaseExpression:
        return Number(p.NUMBER)

    @ _("TRUE")
    def expression(self, p) -> BaseExpression:
        return Boolean(True)

    @ _("FALSE")
    def expression(self, p) -> BaseExpression:
        return Boolean(False)

    @ _("IDENTIFIER '(' argument ')'")
    def function_call(self, p) -> FunctionExpression:
        return FunctionExpression(p.IDENTIFIER, p.argument)

    @_("IDENTIFIER")
    def variable(self, p) -> Variable:
        return Variable(p.IDENTIFIER)

    @ _("expression")
    def argument(self, p) -> FunctionArgument:
        return FunctionArgument(p.expression)

    @ _("argument ',' expression")
    def argument(self, p) -> FunctionArgument:
        return p.argument + p.expression

    def error(self, p) -> NoReturn:
        if p is None:
            raise ParseError(f"Incomplete expression.")

        raise ParseError(f"Invalid expression. Error occurred in position {p.index}")
