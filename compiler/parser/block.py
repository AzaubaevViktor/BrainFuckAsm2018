from typing import List, Union

from ..lexer import Line


class Block(Line):
    def __init__(self, parent: Union["Block", None], line: Line):
        self.parent = parent
        self.line = line
        self.inside: List[Block] = []

    def append(self, block: "Block"):
        self.inside.append(block)

    @property
    def level(self):
        return self.line.level

    @property
    def func(self):
        return self.line.func

    @property
    def args(self):
        return self.line.args

    @level.setter
    def level(self, value):
        self.line.level = value

    def beauty_str(self, indent=None):
        indent = indent or self.level
        i = "    " * indent
        s = f"{i}{self.func} {' '.join(self.args)}\n"
        for block in self.inside:
            s += block.beauty_str(indent + 1)
        return s

