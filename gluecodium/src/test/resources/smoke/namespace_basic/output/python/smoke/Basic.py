

from __future__ import annotations



from _native_base import _NativeBase

import generated


class Basic(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def basic_method(input_string: str) -> str:
        """"""
        native_result = generated.Basic.basic_method(input_string)
        return str(native_result)

