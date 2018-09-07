from typing import Iterable

from .parser import Parser
from .lexer import Lexer
from .translator import Translator


class Compiler:
    def __init__(self, lines: Iterable[str]):
        self.lines = Lexer(lines).lines
        self.root_block = Parser(self.lines).root
        self.code = Translator(self.root_block).code
