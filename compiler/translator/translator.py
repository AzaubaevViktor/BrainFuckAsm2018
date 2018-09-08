from typing import List, Type

from ..lexer import Line
from ..parser import Block
from .namespace import NameSpace
from .func import BuiltinFunction, BuiltinMacro, BuiltinBlock, GeneratedBlockFunction, Function


class Translator:
    def __init__(self, root_block: Block):
        self.root = root_block
        self.ns_root = NameSpace(None)
        self.code = self._compile(self.ns_root, self.root.inside)

    def _compile(self, namespace: NameSpace, lines: List[Line]):
        ns = namespace
        code = ""
        for line in lines:
            Func: Type[BuiltinFunction] = ns.get(line.func, Function)
            func = Func(ns, line.args)

            if isinstance(line, Line):
                if isinstance(func, BuiltinFunction):
                    code += func.build()
                elif isinstance(func, GeneratedBlockFunction):
                    # добавить функции для очистки кадра стека
                    child_ns = ns.create_child()
                    for var_name, obj in func.args.items():
                        child_ns.add(var_name, obj)

                    code += self._compile(child_ns, func.CODE)
                    # переместить результат выполнения функции в текущий ns
                    child_ns.delete_regs()
            if isinstance(line, Block):
                if isinstance(func, BuiltinBlock):
                    code += func.build(line.inside)



        return code



