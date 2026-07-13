

from __future__ import annotations

from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool


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

