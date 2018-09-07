from ..lexer import Token
from ..error import CompileError
from .namespace import NameSpace


class TType:
    pass


class TNum(TType):
    def __init__(self, ns: NameSpace, token: Token):
        self.ns = ns
        self.token = token
        self.value = None
        self._check()

    def _check(self):
        try:
            self.value = int(self.token)
        except ValueError:
            raise CompileError("translator", None, f"`{self.raw}` не является числом.")


class TAddress(TType):
    def __init__(self, ns: NameSpace, token: Token):
        self.ns = ns
        self.token = token
        self.value = None
        self._check()

    def _check(self):
        text = self.token.text

        try:
            if text.startswith(":"):
                self.value = int(text[1:])
                return
        except ValueError:
            pass

        try:
            self.value = self.ns.get_register_address(self.token)
            return
        except CompileError:
            pass

        raise CompileError(
            "translator", self.token,
            f"`{self.token}` не является адресом. Правильный формат: `:<int>` или имя регистра")


class TRegister(TType):
    def __init__(self, ns: NameSpace, token: Token):
        self.ns = ns
        self.token = token
        self.value = None
        self._check()

    def _check(self):
        self.value = self.ns.get_register_address(self.token)


class TString(TType):
    def __init__(self, ns: NameSpace, token: Token):
        self.ns = ns
        self.token = token
        self.value = None
        self._check()

    def _check(self):
        self.value = self.token.text
