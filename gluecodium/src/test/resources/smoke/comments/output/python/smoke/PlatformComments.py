

from __future__ import annotations

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError


from _native_base import _NativeBase

import generated


class PlatformComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        """This is some very useless method that ."""
        return self._native.do_nothing()

    def do_magic(self):
        """"""
        return self._native.do_magic()

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input or \esc@pe{s}."""
        return self._native.some_method_with_all_comments(input)

    def some_deprecated_method(self):
        """"""
        return self._native.some_deprecated_method()
from enum import Enum


class SomeEnum(Enum):
    """"""

    USELESS = 0
    USEFUL = 1


