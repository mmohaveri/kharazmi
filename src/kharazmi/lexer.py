from sly import Lexer
from sly.lex import Token

from .exceptions import LexError


class EquationLexer(Lexer):
    tokens = {
        NUMBER,  # type: ignore
        IDENTIFIER,  # type: ignore
        PLUS,  # type: ignore
        MINUS,  # type: ignore
        TIMES,  # type: ignore
        DIVIDE,  # type: ignore
        POWER,  # type: ignore
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
