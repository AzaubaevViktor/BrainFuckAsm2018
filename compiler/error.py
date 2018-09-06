class CompileError(Exception):
    def __init__(self, level, line, pos, msg="___"):
        self.level = level
        self.line = line
        self.pos = pos
        self.msg = msg

    def __str__(self):
        return f"Error on level `{self.level}`, on line {self.line}, on pos {self.pos}, msg:{self.msg}"
