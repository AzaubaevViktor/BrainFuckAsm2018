
from os import path
from typing import List, Type, Union

from ..error import CompileError
from ..lexer import Line, Lexer
from ..parser import Block, Parser
from .namespace import NameSpace
from .func import BuiltinFunction, BuiltinMacro, BuiltinBlock, GeneratedBlockFunction, Function, \
    GeneratedMacroBlockFunction


def _get_filename(file_name_w_ext):
    file_name = file_name_w_ext.split(".")
    if len(file_name) == 1:
        return file_name[0]
    else:
        return ".".join(file_name[:-1])


class CompiledFile:
    def __init__(self, file_path: Union[str, "Token"]):
        from ..lexer import Token
        self.token = None
        if isinstance(file_path, Token):
            self.token = file_path
            file_path = file_path.text
        self.filepath = file_path
        self.file_name = path.basename(file_path)[1]
        f = self._finder()
        self.raw_lines = f.readlines()
        f.close()
        self.params = self._find_params(self.raw_lines)

    def compile(self):
        lexer = Lexer(self.raw_lines, self.filepath)

        self.lines = lexer.lines
        self.root_block = Parser(self.lines).root
        translator = Translator(self.root_block)
        self.code = translator.code
        self.ns = translator.ns_root
        self.module_name = _get_filename(self.file_name)

    def _find_params(self, lines):
        params = {}
        for line in lines:
            line = line.strip()
            if not line or line[0] != "#":
                continue
            cmt = line[1:]

            if cmt and cmt[0] == "[" and cmt[-1] == "]":
                cmt = cmt[1:-1]
                key, *value = cmt.split(":")
                value = ":".join(value)
                params[key.strip()] = value.strip()
        return params

    def _finder(self):
        if self.token:
            # find in lib
            self.filepath = path.join("./compiler/lib", self.token.text + ".br")

        return open(self.filepath, "rt")


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
            try:
                func = Func(ns, line.args)
            except CompileError as e:
                if e.token is None:
                    e.pop()
                    e.add_to_stacktrace(line.end)
                raise e

            if isinstance(line, Line):
                if isinstance(func, BuiltinFunction):
                    code += func.build()
                elif isinstance(func, GeneratedBlockFunction):
                    # добавить функции для очистки кадра стека
                    child_ns = ns.create_child()
                    for var_name, obj in func.args.items():
                        child_ns.add(var_name, obj)

                    try:
                        code += self._compile(child_ns, func.CODE)
                    except CompileError as e:
                        e.add_to_stacktrace(line)
                        raise e
                    # переместить результат выполнения функции в текущий ns
                    child_ns.delete_regs()
            if isinstance(line, Block):
                if isinstance(func, BuiltinBlock):
                    code += func.build(line.inside)
                elif isinstance(func, GeneratedMacroBlockFunction):
                    # добавить функции для очистки кадра стека
                    child_ns = ns.create_child()
                    for var_name, obj in func.args.items():
                        child_ns.add(var_name, obj)

                    func.build(line.inside)
                    try:
                        code += self._compile(child_ns, func.CODE)
                    except CompileError as e:
                        e.add_to_stacktrace(line)
                        raise e

                    # переместить результат выполнения функции в текущий ns
                    child_ns.delete_regs()



        return code
