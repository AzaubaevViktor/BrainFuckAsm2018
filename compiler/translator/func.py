from typing import List, Tuple

from ..error import CompileError
from ..lexer import Token
from .arg_types import TType, TNum, TAddress
from .namespace import NameSpace


class BuiltinFunction:
    NAME = ""
    ARGS = []

    def __init__(self, ns: NameSpace, args: List[Token]):
        if not self.NAME:
            raise AttributeError("Need attribute NAME for class!")
        self.ns = ns
        self.args = self._args_apply(args)

    def _args_apply(self, args: List[Token]):
        if len(args) != len(self.ARGS):
            arg_err = args[-1] if args else None
            raise CompileError("translator", arg_err, "Argument count do not match")

        ta: List[TType] = []
        for Type, arg in zip(self.ARGS, args):
            ta.append(Type(self.ns, arg))
        return tuple(ta)

    def _build(self, args: Tuple[TType, ...]):
        raise NotImplementedError("Нужно заимплеменитровать!")

    def build(self):
        return self._build(self.args)


class BfAdd(BuiltinFunction):
    NAME = "bf_add"
    ARGS = (TNum, )

    def _build(self, args):
        num: TNum = args[0]

        if num.value > 0:
            return "+" * num.value
        elif num.value < 0:
            return "-" * -num.value
        else:
            return ""


class BfMov(BuiltinFunction):
    NAME = "bf_mov"
    ARGS = (TAddress, TAddress)

    def _build(self, args: Tuple[TAddress, TAddress]):
        to = args[0].addr
        fr = args[1].addr

        if to < fr:
            return "<" * (fr - to)
        elif to > fr:
            return ">" * (to - fr)
        else:
            return ""


class BfPrint(BuiltinFunction):
    NAME = "bf_print"
    ARGS = ()

    def _build(self, args):
        return "."


class BfRead(BuiltinFunction):
    NAME = "bf_read"
    ARGS = ()

    def _build(self, args):
        return ","


class BfCycleOp(BuiltinFunction):
    NAME = "bf_cycle_op"
    ARGS = ()

    def _build(self, args):
        return "["


class BfCycleCl(BuiltinFunction):
    NAME = "bf_cycle_cl"
    ARGS = ()

    def _build(self, args):
        return "]"


