from typing import Any

from ..lexer import Token
from ..error import CompileError


class TType:
    pass


class TNum(TType):
    def __init__(self, raw: Token):
        self.raw = raw
        self.value = None
        self._check()

    def _check(self):
        try:
            self.value = int(self.raw)
        except ValueError:
            raise CompileError("translator", None, f"`{self.raw}` не является числом.")


class TAddress(TType):
    def __init__(self, raw: str):
        self.raw = raw
        self.addr = None
        self._check()

    def _check(self):
        success = False

        try:
            if self.raw[0] == ":":
                self.addr = int(self.raw[1:])
                success = True
        except ValueError:
            pass

        if not success:
            raise CompileError(None, None, None, f"`{self.raw}` не является адресом. Правильный формат: `:<int>`")
