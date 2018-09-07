class CompileError(Exception):
    def __init__(self, level, line_or_token, msg="___", pos=None):
        self.level = level
        self.line = None
        self.token = None
        self.pos = pos or 0

        from .lexer import Line, Token
        if isinstance(line_or_token, Line):
            self.line = line_or_token
        elif isinstance(line_or_token, Token):
            self.token = line_or_token
            self.line = self.token.line
            self.pos = self.token.pos

        self.line_or_token = line_or_token
        self.msg = msg

    def __str__(self):
        return f"Error on level `{self.level}`, on line {self.line}, on pos {self.pos}, msg:{self.msg}"
