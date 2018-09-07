from typing import Union, Dict, Type

from ..error import CompileError
from ..lexer import Token
from .register_store import RegisterStore


class NameSpace:
    STACK_FRAME = ("A", "B", "R", "Cmp", "I", "O", "P", "F")

    def __init__(self, parent: Union["NameSpace", None]):
        self.parent = parent
        self.rs = RegisterStore() if parent is None else parent.rs

        self.rs.create_frame(self.STACK_FRAME)
        self.functions: Dict[str, Type] = {}
        self._init_functions()

    def _init_functions(self):
        if self.parent is None:
            from .func import BfAdd, BfMov, BfPrint, BfRead, BfCycleOp, BfCycleCl, Reg, UnReg
            self.functions = {
                'bf_add': BfAdd,
                'bf_mov': BfMov,
                "bf_print": BfPrint,
                "bf_read": BfRead,
                "bf_cycle_op": BfCycleOp,
                "bf_cycle_cl": BfCycleCl,
                "reg": Reg,
                "unreg": UnReg
            }

    def get_func(self, token: Token) -> Type:
        if token.text not in self.functions:
            if self.parent:
                return self.parent.get_func(token)
            else:
                raise CompileError("translator", token, f"Function {token} not found")
        else:
            return self.functions[token.text]

    def get_register_address(self, token: Token) -> int:
        return self.rs.get(token)

    def create_register(self, token: Token):
        self.rs.create(token)

    def delete_register(self, token: Token):
        self.rs.delete(token)

