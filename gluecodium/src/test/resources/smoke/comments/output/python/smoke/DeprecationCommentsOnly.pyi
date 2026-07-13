

from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool

from _native_base import _NativeBase


class DeprecationCommentsOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def some_method_with_all_comments(self, input: str) -> bool:
        """"""
        return self._native.some_method_with_all_comments(input)


    @property
    def is_some_property(self) -> bool:
        """"""
        return self._native.is_some_property


