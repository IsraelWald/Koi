from typing import Any, Dict, Optional

from typing_extensions import Self

from .token import Token
from .koi_runtime_error import KoiRuntimeError

class Environment:
    def __init__(self, parent: Optional[Self]):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise KoiRuntimeError(name, f"Undefined variable {name.lexeme!r}")
    
    