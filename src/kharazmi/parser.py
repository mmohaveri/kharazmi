from sly import Parser

from .exceptions import ParseError
from .models import Function, Number, Variable, FunctionArgument
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

    def parse(self, inp: str):
        return super().parse(self.lexer.tokenize(inp))

    tokens = EquationLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", TIMES, DIVIDE),
        ("left", POWER),
        ('right', UMINUS),
    )

    start = 'expression'

    @_("expression PLUS expression")
    def expression(self, p):
        return p.expression0 + p.expression1

    @_("expression MINUS expression")
    def expression(self, p):
        return p.expression0 - p.expression1

    @_("expression TIMES expression")
    def expression(self, p):
        return p.expression0 * p.expression1

    @_("expression DIVIDE expression")
    def expression(self, p):
        return p.expression0 / p.expression1

    @_("expression POWER expression")
    def expression(self, p):
        return p.expression0 ** p.expression1

    @_("'(' expression ')'")
    def expression(self, p):
        return p.expression

    @_("MINUS expression %prec UMINUS")
    def expression(self, p):
        return -p.expression

    @_("NUMBER")
    def expression(self, p):
        return Number(p[0])

    @_("IDENTIFIER")
    def expression(self, p):
        return Variable(p[0])

    @_("IDENTIFIER '(' argument ')'")
    def expression(self, p):
        return Function(p[0], p[2])

    @_("expression")
    def argument(self, p):
        return FunctionArgument(p.expression)

    @_("argument ',' expression")
    def argument(self, p):
        return p.argument + p.expression

    def error(self, p):
        if p is None:
            raise ParseError(f"Incomplete expression.")

        raise ParseError(f"Invalid expression. Error occurred in position {p.index}")
