from __future__ import annotations

from typing import Any, Dict, Optional
from typing_extensions import Self

from .token import Token
from .koi_runtime_error import KoiRuntimeError


class Environment:
    def __init__(self, parent: Optional[Self]) -> None:
        self.values: Dict[str, Any] = dict()
        self.parent = parent

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def _ancestor(self, distance: int) -> Self:
        environment: Self = self

        for _ in range(distance):
            environment = environment.parent  # type: ignore

        return environment

    def get_at(self, distance: int, name: str) -> Any:
        """Return a variable at distance"""
        return self._ancestor(distance=distance).values.get(name)

    def get(self, name: Token) -> Any:
        try:
            return self.values[name]
        except KeyError:
            # Ignore this and try to get from an ancestor
            pass

        if self.parent:
            self.parent.get(name)

        raise KoiRuntimeError(name, f"Undefined name {name.lexeme!r}")

    def assign(self, name: Token, value: Any) -> None:
        """Assign a new value to an existing variable.
        var a = 10 // This calls define
        a = 11     // This calls assign
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise KoiRuntimeError(name, f"Undefined name {name.lexeme!r}")

    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self._ancestor(distance=distance).values[name.lexeme] = value
