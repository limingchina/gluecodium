

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DeprecationCommentsOnly(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, DeprecationCommentsOnly):
            super().__init__(native)
        else:
            super().__init__(generated.DeprecationCommentsOnly())

    def some_method_with_all_comments(self, input: str) -> bool:
        """"""
        return self._native.some_method_with_all_comments(input)


    @property
    def is_some_property(self) -> bool:
        """"""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value
from enum import Enum


class SomeEnum(Enum):
    """"""

    USELESS = 0



VERY_USEFUL = True

