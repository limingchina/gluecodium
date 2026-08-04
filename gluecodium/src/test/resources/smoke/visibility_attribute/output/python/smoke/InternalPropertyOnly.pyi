

from enum import Enum
import typing

class InternalPropertyOnly:

    @property
    def __foo(self) -> str:
        ...

    @__foo.setter
    def __foo(self, value: str) -> None:
        ...


