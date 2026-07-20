

from __future__ import annotations


from _native_base import _NativeBase

import generated


class OuterStructInnerClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo_bar(self) -> set[str]:
        """"""
        return self._native.foo_bar()

