

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class InternalClassWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo_bar(self):
        """"""
        return _wrap(self._native.foo_bar(), None)

    @staticmethod
    def make(*args, **kwargs) -> InternalClassWithFunctions:
        """"""
        native_result = generated.smoke_InternalClassWithFunctions.make(*[_unwrap(a) for a in args])
        return _get_or_create_wrapper(native_result, InternalClassWithFunctions)


