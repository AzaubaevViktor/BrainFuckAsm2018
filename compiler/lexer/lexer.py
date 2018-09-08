from typing import List, Iterable

from .line import Line


class Lexer:
    def __init__(self, lines: Iterable[str], file_path: str):
        self.lines: List[Line] = []
        for n, line in enumerate(lines):
            line = Line(file_path, n, line)
            if line:
                self.lines.append(line)
