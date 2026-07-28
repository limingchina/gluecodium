

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.forward.InnerClassForwardDeclarationsInnerInterface2 import InnerClassForwardDeclarationsInnerInterface2

from _native_base import _NativeBase

import generated


class InnerClassForwardDeclarationsInnerClass2InnerInnerClass2(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def bar(self, arg: InnerClassForwardDeclarationsInnerInterface2):
        """"""
        return _wrap(self._native.bar(_unwrap(arg, InnerClassForwardDeclarationsInnerInterface2)), None)

