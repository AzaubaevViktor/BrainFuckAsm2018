class CompileError(Exception):
    def __init__(self, level, line_or_token, msg="___", pos=None):
        self.stacktrace = []

        self.level = level

        self.add_to_stacktrace(line_or_token, pos)
        self.msg = msg
        self.line, self.token, self.pos = self.stacktrace[0]

    def add_to_stacktrace(self, line_or_token, pos=None):
        line = None
        token = None
        pos = pos or 0

        from .lexer import Line, Token
        if isinstance(line_or_token, Line):
            line = line_or_token
        elif isinstance(line_or_token, Token):
            token = line_or_token
            line = token.line
            pos = token.pos

        self.stacktrace.append([
            line, token, pos
        ])

    def __str__(self):
        s = f"Compilation Error on level `{self.level}`:"
        for line, token, pos in self.stacktrace[::-1]:
            s += f"""
  File `{line.file_path}`, line {line.n}:{pos}
    {line.raw}
    {" " * pos}{"^" * (len(token.text) if token else 0)}"""
        s += f"\n{self.msg}"
        return s
