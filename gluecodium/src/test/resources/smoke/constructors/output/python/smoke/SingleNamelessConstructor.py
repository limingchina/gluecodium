

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SingleNamelessConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def create() -> SingleNamelessConstructor:
        """"""
        native_result = generated.SingleNamelessConstructor.create()
        return SingleNamelessConstructor(native_result)

