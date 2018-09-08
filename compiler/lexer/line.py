from typing import Tuple, List, Union

from compiler import CompileError


class Token:
    def __init__(self, line: Union["Line", None], pos: Union[int, None], text: str):
        self.line = line
        self.pos = pos
        self.text = text

    def __int__(self):
        return int(self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"<Token {self.line.n if self.line else '?'}:{self.pos or '?'} `{self.text}`"


class Line:
    def __init__(self, file_path: str, line_number: int, data: str):
        self.file_path = file_path
        self.n = line_number
        self.raw = data = data.rstrip()

        spaces = len(data) - len(data.lstrip())
        if spaces % 4 != 0:
            raise CompileError('lexer', self, "Количество пробелов не кратно 4м", pos=spaces - 1)

        self.level = spaces // 4

        data = data.strip()

        data, *self.comment = data.split("#")
        self.comment = " ".join(self.comment)
        if self.comment:
            self.comment = self.comment[1:]

        args = self.tokenize(data)

        self.func: Token = args[0] if args else None
        self.args: List[Token] = args[1:]

    def __bool__(self):
        return bool(self.func)

    def __str__(self):
        return f"<Line#{self.n}[{self.level}], `{self.raw}`"

    def __repr__(self):
        return str(self)

    def tokenize(self, data):
        tokens = []
        cur = ""
        pos = 0
        for i, c in enumerate(data):  # type: int, str
            if not c.isspace():
                if not cur:
                    pos = i
                cur += c
            elif cur:
                tokens.append(Token(self, pos, cur))
                cur = ""

        if cur:
            tokens.append(Token(self, pos, cur))

        return tokens

    def beauty_str(self, indent):
        i = "    " * indent
        return f"{i}{self.func} {' '.join(map(str, self.args))}\n"

