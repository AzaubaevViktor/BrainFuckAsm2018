from typing import Union

from ..error import CompileError
from ..lexer import Token
from .register_store import RegisterStore



class NameSpace:
    STACK_FRAME = ("A", "B", "R", "Cmp", "I", "O", "P", "F")

    def __init__(self, parent: Union["NameSpace", None]):
        self.parent = parent
        self.rs = RegisterStore() if parent is None else parent.rs

        self.rs.create_frame(self.STACK_FRAME)
        self.functions = {}
        self._init_functions()

    def _init_functions(self):
        if self.parent is None:
            from .func import Add
            self.functions = {
                'bf_add': Add
            }

    def get_func(self, name: Token):
        if name.text not in self.functions:
            if self.parent:
                return self.parent.get_func(name)
            else:
                raise CompileError("translator", name, f"Function {name} not found")
        else:
            return self.functions[name.text]

