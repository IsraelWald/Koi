from ..koi_callable import KoiCallable
from typing import List


class Length(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        return len(args[0])

    def __repr__(self) -> str:
        return "<native function length(string)>"
