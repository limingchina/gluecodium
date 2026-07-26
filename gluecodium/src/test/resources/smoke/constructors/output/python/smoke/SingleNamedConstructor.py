

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class SingleNamedConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> SingleNamedConstructor:
        """"""
        native_result = generated.smoke_SingleNamedConstructor.create()
        return SingleNamedConstructor(native_result)

