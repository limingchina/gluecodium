

from package.Interface import Interface
from package.Types import Types
from enum import Enum
import typing
from typing import Optional

class Class(
    Interface):

    @staticmethod
    def constructor() -> Class:
        ...

    def fun(self, double: list[Types.Struct]) -> Types.Struct:
        ...

    @property
    def property(self) -> Types.Enum:
        ...

    @property.setter
    def property(self, value: Types.Enum) -> None:
        ...
