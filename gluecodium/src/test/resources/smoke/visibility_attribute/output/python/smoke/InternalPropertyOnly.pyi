

from enum import Enum
import typing
from typing import Optional

class InternalPropertyOnly:

    @property
    def _foo(self) -> str:
        ...

    @_foo.setter
    def _foo(self, value: str) -> None:
        ...
