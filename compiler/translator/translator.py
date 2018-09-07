from typing import List, Type

from ..lexer import Line
from ..parser import Block
from .namespace import NameSpace
from .func import BuiltinFunction


class Translator:
    def __init__(self, root_block: Block):
        self.root = root_block
        self.ns_root = NameSpace(None)
        self.code = self._compile(self.ns_root, self.root.inside)

    def _compile(self, namespace: NameSpace, lines: List[Line]):
        ns = namespace
        code = ""
        for line in lines:
            if isinstance(line, Line):
                if line.is_comment:
                    continue
                Func: Type[BuiltinFunction] = ns.get_func(line.func)
                func = Func(ns, line.args)
                code += func.build()

        return code



