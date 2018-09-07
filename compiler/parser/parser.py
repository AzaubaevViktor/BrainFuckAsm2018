from typing import List

from .block import Block
from ..lexer import Line


class Parser:
    def __init__(self, lexer_lines: List[Line]):
        self.lines = []
        self.cur_level = 0
        self.root = Block(None, Line(-1, ""))
        self.root.level = -1
        block = self.root
        for line in lexer_lines:

            if block.level + 1 == line.level:
                block.append(line)
            elif block.level + 2 == line.level:
                prev_line = block.pop()
                new_block = Block(block, prev_line)
                block.append(new_block)
                block = new_block
                new_block.append(line)
            elif block.level >= line.level:
                for i in range(block.level - line.level + 1):
                    block = block.parent
                block.append(line)

