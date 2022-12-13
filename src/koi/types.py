from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Any, List
from .tokens import Token


class TypeVisitor(ABC):
    @abstractmethod
    def visit_string_type(self, string: StringType):
        raise NotImplementedError


class BaseType(ABC):
    @abstractmethod
    def accept(self, visitor: TypeVisitor):
        raise NotImplementedError


class StringType(BaseType):
    def __init__(self, value: str) -> None:
        self.value = value

    def accept(self, visitor: TypeVisitor):
        return visitor.visit_string_type(self.value)
