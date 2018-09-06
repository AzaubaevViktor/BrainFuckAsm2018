from typing import List

from ..lexer import Line


class Parser:
    def __init__(self, lexer_lines: List[Line]):
        self.lines = []
        self.cur_level = 0
        self.root = Block()
        for line in lexer_lines:
            if