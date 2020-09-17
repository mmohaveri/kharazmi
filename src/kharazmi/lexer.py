from sly import Lexer
from sly.lex import Token

from .exceptions import LexError


class EquationLexer(Lexer):
    tokens = {
        NUMBER,
        IDENTIFIER,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        POWER,
    }

    literals = ["(", ")", ","]
    ignore = " \t"

    IDENTIFIER = r"[a-zA-Z_][a-zA-Z_0-9]*"
    NUMBER = r"\d+(\.\d*)?((\+|\-)\d+(\.\d*)?j)?"
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    POWER = r'\^'

    def error(self, token: Token):
        raise LexError(f"Invalid token '{token.value[0]}'")
