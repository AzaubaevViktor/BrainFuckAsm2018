
from os import path
from typing import List, Type

from ..lexer import Line, Lexer
from ..parser import Block, Parser
from .namespace import NameSpace
from .func import BuiltinFunction, BuiltinMacro, BuiltinBlock, GeneratedBlockFunction, Function


def _get_filename(file_name_w_ext):
    file_name = file_name_w_ext.split(".")
    if len(file_name) == 1:
        return file_name[0]
    else:
        return ".".join(file_name[:-1])


class CompiledFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = path.basename(file_path)[1]
        f = self._finder(self.file_path)
        self.raw_lines = f.readlines()
        lexer = Lexer(self.raw_lines, file_path)

        self.lines = lexer.lines
        self.params = self._find_params(lexer.comment_lines)
        self.root_block = Parser(self.lines).root
        self.code = Translator(self.root_block).code
        self.module_name = _get_filename(self.file_name)

    def _find_params(self, lines):
        params = {}
        for line in lines:
            cmt = line.comment
            if cmt and cmt[0] == "[" and cmt[-1] == "]":
                cmt = cmt[1:-1]
                key, *value = cmt.split(":")
                value = ":".join(value)
                params[key.strip()] = value.strip()
        return params

    def _finder(self, file_name):
        return open(file_name, "rt")


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
