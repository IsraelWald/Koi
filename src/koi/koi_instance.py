from typing import Any
from .tokens import Token
from .koi_runtime_error import KoiRuntimeError


class KoiInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def __repr__(self) -> str:
        return f"<instance of class {self.klass.name!r}>"

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise KoiRuntimeError(name, f"Undefined property {name.lexeme!r}")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value
