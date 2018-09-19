from collections import OrderedDict
from typing import List, Tuple, Dict, Type

from ..error import CompileError
from ..lexer import Token, Line
from .var_types import VType, TNum, TAddress, TString, TRegister, ttypes, TType, TName
from .namespace import NameSpace


class Function:
    """Базовая функция"""
    NAME = ""
    ARGS = ()
    LINKED_NAMESPACE = None

    def __init__(self, ns: NameSpace, args: List[Token]):
        if not self.NAME:
            raise AttributeError("Need attribute NAME for class!")
        self.ns = ns
        self.args = self._args_apply(args)

    def _args_apply(self, args: List[Token], ARGS=None):
        ARGS = ARGS or self.ARGS

        if len(args) > len(ARGS):
            raise CompileError("translator", args[len(ARGS)], "Too many arguments")
        elif len(args) < len(ARGS):
            raise CompileError("translator", None, f"`{ARGS[len(args)].NAME}` variable expected, `None` in fact")

        ta: List[VType] = []
        for Type, arg in zip(ARGS, args):
            ta.append(Type(arg, ns=self.ns))
        return tuple(ta)

    def build(self, *args):
        pass


class BuiltinFunction(Function):
    """Встроенна функция"""
    ARGS = []

    def _build(self, args: Tuple[VType, ...]):
        raise NotImplementedError("Нужно заимплеменитровать!")

    def build(self) -> List[Function]:
        _r = self._build(self.args)
        if _r is None:
            return []

        if isinstance(_r, str):
            return [BfRaw(self.ns, [Token(None, None, _r)])]

        if not isinstance(_r, list):
            raise ValueError(_r, "Not list!")

        return _r


class _GenBlockF(Function):
    def _args_apply(self, args: List[Token], ARGS=None):
        ARGS = [a[1] for a in self.ARGS]
        args = super()._args_apply(args, ARGS)
        args = {name: result for (name, _) , result in zip(self.ARGS, args)}
        return args


class GeneratedBlockFunction(_GenBlockF):
    NAME = ""
    ARGS = ()
    CODE = []


class GeneratedMacroBlockFunction(_GenBlockF):
    NAME = ""
    ARGS = ()
    CODE = []

    def build(self, line_inside: List[Line]):
        class DOLLAR_NewFunc(GeneratedBlockFunction):
            NAME = f"${self.NAME}"
            ARGS = ()
            CODE = line_inside

        DOLLAR_NewFunc.__name__ = f"GeneratedDollar${DOLLAR_NewFunc.NAME}Function"

        self.ns.add(Token(None, None, f"{DOLLAR_NewFunc.NAME}"), DOLLAR_NewFunc)


class BuiltinBlockFunction(Function):
    pass



class BfRaw(BuiltinFunction):
    NAME = "bf_raw"
    ARGS = (TString)

    def _build(self, args: Tuple[TString]):
        return args[0].value


class BfAdd(BuiltinFunction):
    NAME = "bf_add"
    ARGS = (TNum, )

    def _build(self, args):
        num: TNum = args[0]

        if num.value > 0:
            return self.ns, "+" * num.value
        elif num.value < 0:
            return self.ns, "-" * -num.value
        else:
            return None


class BfMov(BuiltinFunction):
    NAME = "bf_mov"
    ARGS = (TAddress, TAddress)

    def _build(self, args: Tuple[TAddress, TAddress]):
        to = args[0].value
        fr = args[1].value

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


class Reg(BuiltinFunction):
    NAME = "reg"
    ARGS = (TName, )

    def _build(self, args: Tuple[TName]):
        token = args[0].token
        self.ns.add(token, -1, register=True)
        return ""


class UnReg(BuiltinFunction):
    NAME = "unreg"
    ARGS = (TRegister, )

    def _build(self, args: Tuple[TRegister]):
        token = args[0].token
        self.ns.delete(token)
        return ""

# Block function


class MultiArgFunction(BuiltinBlockFunction):
    def _args_apply(self, args: List[Token], ARGS=None):
        if len(args) % 2 != 1:
            arg_err = args[-1] if args else None
            raise CompileError("translator", arg_err, "Argument count do not match (need 2n+1)")

        func_name_token = TName(args[0])
        func_args: Dict[str, Type[VType]] = OrderedDict()

        for name, type_name in zip(args[1::2], args[2::2]):
            _type = TType(type_name).value

            func_args[name] = _type

        self.func_name_tp = func_name_token
        self.func_args = func_args


class Macro(MultiArgFunction):
    NAME = "macro"

    def build(self, lines: List[Line]):
        class NewFunction(GeneratedBlockFunction):
            NAME = self.func_name_tp.value
            ARGS = tuple(self.func_args.items())

            CODE = lines
            LINKED_NAMESPACE = self.ns

        NewFunction.__name__ = f"Generated{NewFunction.NAME}Function"

        self.ns.add(self.func_name_tp.token, NewFunction)
        return ""


class MacroBlock(MultiArgFunction):
    NAME = "macroblock"

    def build(self, lines: List[Line]):
        class NewFunction(GeneratedMacroBlockFunction):
            NAME = self.func_name_tp.value
            ARGS = tuple(self.func_args.items())

            CODE = lines
            LINKED_NAMESPACE = self.ns

        NewFunction.__name__ = f"Generated{NewFunction.NAME}BlockFunction"

        self.ns.add(self.func_name_tp.token, NewFunction)

        return ""


class Include(BuiltinFunction):
    NAME = "include"
    ARGS = (TString, )

    def _build(self, args: Tuple[TString]):
        module_name = args[0].token

        from compiler import CompiledFile
        cf = CompiledFile(module_name)
        cf.compile()
        self.ns.add_module(module_name, cf.ns)
        return cf.code


"return"  # возвращает значие вниз по стеку
"clear_frame"  # очистит текущий кадр стека
"global"  # Достаёт переменную из уровня ниже (и переименовывает её)
