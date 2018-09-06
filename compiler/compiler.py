from typing import Iterable

from .lexer import Lexer


class Compiler:
    def __init__(self, lines: Iterable[str]):
        self.lines = Lexer(lines).lines
