

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.forward.InnerClassForwardDeclarationsInnerClass2InnerInnerClass2 import InnerClassForwardDeclarationsInnerClass2InnerInnerClass2

from _native_base import _NativeBase

import generated


class InnerClassForwardDeclarationsInnerClass2InnerInnerClass1(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def foo(self) -> InnerClassForwardDeclarationsInnerClass2InnerInnerClass2:
        return _wrap(self._native.foo(), InnerClassForwardDeclarationsInnerClass2InnerInnerClass2)

