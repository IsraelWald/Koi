from typing import Any, Dict, Optional

from typing_extensions import Self

from .token import Token
from .koi_runtime_error import KoiRuntimeError


class Environment:
    def __init__(self, parent: Optional[Self] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.parent != None:
            return self.parent.get(name)
        raise KoiRuntimeError(name, f"Undefined variable {name.lexeme!r}")
    
    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.parent != None:
            self.parent.assign(name, value)
        raise KoiRuntimeError(name, f"Cannot assign to variable {name.lexeme!r} before it was declared.")