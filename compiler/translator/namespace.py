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
        self.modules: Dict[str, "NameSpace"] = {}

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
                BuiltinMacro, BuiltinMacroBlock, BuiltinInclude
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
                "macroblock": BuiltinMacroBlock,
                "include": BuiltinInclude
            })

    def get(self, token: Token, check=None):
        check_name = (check.__name__ if check else None) or 'Object'
        obj_name = token.text
        if "." in obj_name:
            module, obj_name = token.split(".")
            if module.text in self.modules:
                obj = self.modules[module.text].get(obj_name, check)
            else:
                obj = None
        else:
            if obj_name in self.objs:
                obj = self.objs[obj_name]
            elif self.parent:
                obj = self.parent.get(token)
            else:
                raise CompileError("translator", token, f"{check_name} `{token}` not found in namespace")

        if check:
            if isinstance(obj, check):
                return obj

            if isinstance(obj, type):
                if issubclass(obj, check):
                    return obj

            raise CompileError(
                "translator", token,
                f"`{token}` found, but it is {type(obj)}, not `{check_name}` ")

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

    def create_child(self):
        return NameSpace(self)

    def add_module(self, name: Token, ns: "NameSpace"):
        if name in self.modules:
            raise CompileError("translator", name, f"Module `{name}` already exist")
        self.modules[name.text] = ns
