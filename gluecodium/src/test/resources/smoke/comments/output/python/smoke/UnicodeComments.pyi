

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError
from smoke.bool import bool


from _native_base import _NativeBase

import generated


class UnicodeComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    Süßölgefäß
    def some_method_with_all_comments(self, input: str) -> bool:
        """Süßölgefäß"""
        return self._native.some_method_with_all_comments(input)

