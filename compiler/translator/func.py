from typing import List, Tuple

from ..error import CompileError
from ..lexer import Token
from .arg_types import TType, TNum
from .namespace import NameSpace


class BuiltinFunction:
    NAME = ""
    ARGS = []

    def __init__(self, args: List[Token]):
        if not self.NAME:
            raise AttributeError("Need attribute NAME for class!")
        self.args = self._args_apply(args)

    def _args_apply(self, args: List[Token]):
        if len(args) != len(self.ARGS):
            arg_err = args[-1] if args else None
            raise CompileError("translator", arg_err, "Argument count do not match")

        ta: List[TType] = []
        for Type, arg in zip(self.ARGS, args):
            ta.append(Type(arg))
        return tuple(ta)

    def _build(self, ns: NameSpace, args: Tuple[TType]):
        raise NotImplementedError("Нужно заимплеменитровать!")

    def build(self, ns: NameSpace):
        return self._build(ns, self.args)


class Add(BuiltinFunction):
    NAME = "bf_add"
    ARGS = (TNum, )

    def _build(self, ns, args):
        num: TNum = args[0]

        if num.value > 0:
            return "+" * num.value
        elif num.value < 0:
            return "-" * -num.value
        else:
            return ""
