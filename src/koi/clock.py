from koi_callable import KoiCallable
from typing import TYPE_CHECKING, List
from time import time

if TYPE_CHECKING:
    from .interpreter import Interpreter


class Clock(KoiCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: Interpreter, args: List):
        return float(time())

    def __repr__(self) -> str:
        return "<native function clock>"
