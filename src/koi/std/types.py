from ..koi_callable import KoiCallable
from typing import List


class ToInt(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        return int(args[0].value)

    def __repr__(self) -> str:
        return "<native function toInt>"
