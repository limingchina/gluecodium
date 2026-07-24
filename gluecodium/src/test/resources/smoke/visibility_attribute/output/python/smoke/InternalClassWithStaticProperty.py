

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class InternalClassWithStaticProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @staticmethod
    def foo_bar() -> str:
        """"""
        return _wrap(generated.InternalClassWithStaticProperty.foo_bar(), str)

