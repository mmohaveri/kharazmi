from typing import Set
from sly import Lexer  # pyright: ignore [reportMissingTypeStubs]
from sly.lex import Token  # pyright: ignore [reportMissingTypeStubs]


from .exceptions import LexError


class EquationLexer(Lexer):
    tokens: Set[str] = {
        NUMBER,  # pyright: ignore [reportUndefinedVariable]
        IDENTIFIER,  # pyright: ignore [reportUndefinedVariable]
        PLUS,  # pyright: ignore [reportUndefinedVariable]
        MINUS,  # pyright: ignore [reportUndefinedVariable]
        TIMES,  # pyright: ignore [reportUndefinedVariable]
        DIVIDE,  # pyright: ignore [reportUndefinedVariable]
        POWER,  # pyright: ignore [reportUndefinedVariable]
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
