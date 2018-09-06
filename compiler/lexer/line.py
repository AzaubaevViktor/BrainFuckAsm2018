from compiler import CompileError


class Line:
    def __init__(self, line_number: int, data: str):
        self.n = line_number
        self.raw = data = data.rstrip()

        spaces = len(data) - len(data.lstrip())
        if spaces % 4 != 0:
            raise CompileError('lexer', self, spaces - 1, "Количество пробелов не кратно 4м")

        self.level = spaces // 4

        data = data.strip()

        self.is_comment = False
        if data and data[0] == "#":
            self.is_comment = True

        args = [x.strip() for x in data.split() if x.strip()]

        self.func = args[0] if args else ""
        self.args = args[1:]

    def __bool__(self):
        return bool(self.func)

    def __str__(self):
        return f"<Line#{self.n}[{self.level}], `{self.raw}`"

    def __repr__(self):
        return str(self)
