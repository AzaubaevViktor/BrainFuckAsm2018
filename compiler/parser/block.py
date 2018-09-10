from typing import List, Union

from ..lexer import Line


class Block(Line):
    def __init__(self, parent: Union["Block", None], line: Line):
        self.parent = parent
        self.line = line
        self.inside: List[Line] = []

    @property
    def is_inside(self):
        return bool(self.inside)

    def append(self, block: "Line"):
        self.inside.append(block)

    def pop(self)-> Line:
        return self.inside.pop()

    @property
    def level(self):
        return self.line.level

    @property
    def func(self):
        return self.line.func

    @property
    def args(self):
        return self.line.args

    @property
    def end(self):
        return self.line.end

    @level.setter
    def level(self, value):
        self.line.level = value

    def beauty_str(self, indent=None):
        indent = indent or self.level
        i = "    " * indent
        if self.level >= 0:
            s = f"{i}{self.func} {' '.join(map(str, self.args))}\n"
        else:
            s = ""

        for block in self.inside:
            s += block.beauty_str(indent + 1)
        return s

