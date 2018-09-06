from typing import List, Iterable

from .line import Line


class Lexer:
    def __init__(self, lines: Iterable[str]):
        self.lines: List[Line] = []
        for n, line in enumerate(lines):
            line = Line(n, line)
            if line:
                self.lines.append(line)
