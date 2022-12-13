from ..koi_callable import KoiCallable
from typing import List


class Print(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        print(self.stringify(args[0]), end="")

    def _stringify(self, value):
        if value is None:
            return "nil"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif isinstance(value, (float, int)):
            return str(value)
        return str(value)

    def __repr__(self) -> str:
        return "<native function print>"


class Println(KoiCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, args: List):
        print(self.stringify(args[0]))

    def _stringify(self, value):
        if value is None:
            return "nil"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif isinstance(value, (float, int)):
            return str(value)
        return str(value)

    def __repr__(self) -> str:
        return "<native function println>"
