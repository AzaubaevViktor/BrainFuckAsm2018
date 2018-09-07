from typing import List, Dict, Iterable

from ..lexer import Token
from ..error import CompileError


class RegisterStore:
    """
    Выделяет только чётные ячейки памяти, так как нечётные используются для динамической памяти
    """
    def __init__(self):
        self.busy_cells: List[int] = []
        self.stack_frames: List[Dict[str, int]] = []

    def _free_cell(self) -> int:
        """Ищет свободную ячейку"""
        addr = 0
        while True:
            if addr not in self.busy_cells:
                self.busy_cells.append(addr)
                return addr
            addr += 2

    @property
    def _last_frame(self):
        return self.stack_frames[-1]

    def create_frame(self, variables: Iterable[str]):
        frame = {var_name: self._free_cell() for var_name in variables}
        self.stack_frames.append(frame)

    def delete_frame(self):
        last_frame = self.stack_frames.pop()
        for addr in last_frame.values():
            self.busy_cells.remove(addr)

    def get(self, token: Token) -> int:
        name = token.text

        for frame in self.stack_frames[::-1]:
            if name in frame:
                return frame[name]

        raise CompileError("translator", token, f"Register `{name}` not found!")

    def create(self, token: Token):
        name = token.text
        if name in self._last_frame:
            raise CompileError("translator", token, f"Register {name} already exist")
        self._last_frame[name] = self._free_cell()

    def delete(self, token: Token):
        name = token.text
        if name not in self._last_frame:
            raise CompileError("translator", token, f"Register {name} doesn't exist")
        addr = self._last_frame[name]
        del self._last_frame[name]
        self.busy_cells.remove(addr)




