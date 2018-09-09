from typing import Union, Dict, Type

from ..error import CompileError
from ..lexer import Token
from .register_store import RegisterStore


class NameSpace:
    STACK_FRAME = ("A", "B", "R", "Cmp", "I", "O", "P", "F")

    def __init__(self, parent: Union["NameSpace", None]):
        self.parent = parent
        self.rs = RegisterStore() if parent is None else parent.rs

        self.objs = {}

        self.rs.create_frame(self.STACK_FRAME)
        self._init_registers()

        self._init_functions()

    def init_ns(self):
        """Для кода очистки кадра стека"""
        pass

    def deinit_ns(self):
        pass

    def delete_regs(self):
        self.rs.delete_frame()

    def _init_registers(self):
        from compiler.translator.var_types import TRegister
        for name in self.STACK_FRAME:
            token = Token(None, None, name)
            addr = self.rs.get(token)
            self.add(token, addr)

    def _init_functions(self):
        if self.parent is None:
            from .func import BfAdd, BfMov, BfPrint, BfRead, BfCycleOp, BfCycleCl, Reg, UnReg, \
                BuiltinMacro, BuiltinMacroBlock
            self.objs.update({
                'bf_add': BfAdd,
                'bf_mov': BfMov,
                "bf_print": BfPrint,
                "bf_read": BfRead,
                "bf_cycle_op": BfCycleOp,
                "bf_cycle_cl": BfCycleCl,
                "reg": Reg,
                "unreg": UnReg,
                "macro": BuiltinMacro,
                "macroblock": BuiltinMacroBlock
            })

    def get(self, token: Token, check=None):
        obj_name = token.text
        if obj_name in self.objs:
            obj = self.objs[obj_name]
        elif self.parent:
            obj = self.parent.get(token)
        else:
            raise CompileError("translator", token, f"{check or 'Object'} {token} not found in namespace")

        if check:
            if isinstance(obj, check):
                return obj

            if isinstance(obj, type):
                if issubclass(obj, check):
                    return obj

            raise CompileError(
                "translator", token,
                f"{token} found, but it is not {check}, but {type(obj)}")

        return obj

    def add(self, token: Token, obj, register=False):
        if token.text in self.objs:
            raise CompileError("translator", token, f"{token} already exists ({type(self.objs[token.text])}")

        if register:
            obj = self.rs.create(token)

        if isinstance(obj, int):
            from compiler.translator.var_types import TRegister
            obj = TRegister(token, self, obj)
        self.objs[token.text] = obj

    def delete(self, token: Token):
        if token.text not in self.objs:
            raise CompileError("translator", token, f"`{token}` not in this ns to delete")

        value = self.objs[token.text]
        from .var_types import TRegister
        if isinstance(value, TRegister):
            self.rs.delete(token)

        del self.objs[token.text]

    def _add_func(self, func: "Function"):
        self.add(func.NAME, func)

    def _get_func(self, token: Token) -> Type:
        if token.text not in self.functions:
            if self.parent:
                return self.parent.get_func(token)
            else:
                raise CompileError("translator", token, f"Function {token} not found")
        else:
            return self.functions[token.text]

    def _get_register_address(self, token: Token) -> int:
        return self.rs.get(token)

    def _create_register(self, token: Token):
        self.rs.create(token)

    def _delete_register(self, token: Token):
        self.rs.delete(token)

    def create_child(self):
        return NameSpace(self)
