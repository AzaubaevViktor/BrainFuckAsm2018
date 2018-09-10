from typing import List, Iterable

from .line import Line


class Lexer:
    def __init__(self, lines: Iterable[str], file_path: str):
        self.lines: List[Line] = []
        self.comment_lines = []
        for n, line in enumerate(lines):
            line = Line(file_path, n + 1, line)
            if line:
                self.lines.append(line)
            else:
                self.comment_lines.append(line)
