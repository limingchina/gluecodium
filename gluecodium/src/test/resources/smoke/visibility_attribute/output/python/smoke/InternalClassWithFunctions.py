

from __future__ import annotations


from _native_base import _NativeBase

import generated


class InternalClassWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo_bar(self):
        """"""
        return self._native.foo_bar()

    @staticmethod
    def make(*args, **kwargs) -> InternalClassWithFunctions:
        """"""
        native_result = generated.InternalClassWithFunctions.make(*[getattr(a, "_native", a) for a in args])
        return InternalClassWithFunctions(native_result)


