from ..koi_callable import KoiCallable
from .strings import StringInstance
from typing import List


class Input(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        return StringInstance(input(args[0]))

    def __repr__(self) -> str:
        return "<native function input(prompt)>"
