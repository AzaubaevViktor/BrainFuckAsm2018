from typing import Dict, Type, List

from ..lexer import Token
from ..error import CompileError
from .namespace import NameSpace


class VType:
    NAME = ""

    def __init__(self, token: Token, ns: NameSpace = None, *args):
        if not self.NAME:
            raise AttributeError("Need attribute NAME for class!")

        self.ns = ns
        self.token = token
        self.value = None
        self.args = args
        self._check()

    def _try_in_ns(self, cl=None):
        cl = cl or self.__class__

        try:
            self.value = self.ns.get(self.token, cl).value
            return True
        except CompileError:
            return False

    def _check(self):
        raise NotImplementedError("Нужно имплементировать!")

    def __repr__(self):
        return f"<{self.__class__.__name__} `{self.token.text}`:#{self.value}>"


class TNum(VType):
    NAME = "num"

    def _check(self):
        try:
            self.value = int(self.token)
            return
        except ValueError:
            pass

        if self._try_in_ns():
            return

        raise CompileError("translator", self.token, f"`{self.token}` не является числом.")


class TAddress(VType):
    NAME = "address"

    def _check(self):
        text = self.token.text

        try:
            if text.startswith(":"):
                self.value = int(text[1:])
                return
        except ValueError:
            pass

        if self._try_in_ns(TRegister):
            return

        if self._try_in_ns(TAddress):
            return

        raise CompileError(
            "translator", self.token,
            f"`{self.token}` не является адресом. Правильный формат: `:<int>` или имя регистра")


class TRegister(VType):
    NAME = "register"

    def _check(self):
        if self.args:
            self.value = self.args[0]
        else:
            treg: TRegister = self.ns.get(self.token, TRegister)
            self.value = treg.value

class TString(VType):
    NAME = "string"

    def _check(self):
        self.value = self.token.text


ttypes: List[Type[VType]] = [TNum, TAddress, TRegister, TString]
ttypes: Dict[str, Type[VType]] = {tt.NAME: tt for tt in ttypes}


class TType(VType):
    NAME = "type"

    def _check(self):
        try:
            self.value = ttypes[self.token.text]
        except KeyError:
            raise CompileError("translator", self.token, f"Type {self.token} not found!")
