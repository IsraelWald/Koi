from .interpreter import Interpreter
from typing import List


class KoiCallable:
    def arity(self) -> int:
        raise NotImplementedError("Implement the arity function")

    def call(self, interpreter: Interpreter, args: List):
        raise NotImplementedError("Implement the call function")
