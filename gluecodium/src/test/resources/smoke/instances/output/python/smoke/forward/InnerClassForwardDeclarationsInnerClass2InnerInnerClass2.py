

from __future__ import annotations

from smoke.forward.InnerClassForwardDeclarationsInnerInterface2 import InnerClassForwardDeclarationsInnerInterface2

from _native_base import _NativeBase

import generated


class InnerClassForwardDeclarationsInnerClass2InnerInnerClass2(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def bar(self, arg: InnerClassForwardDeclarationsInnerInterface2):
        """"""
        return self._native.bar(arg._native)

