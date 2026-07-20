

import typing

from _native_base import _NativeBase

import generated


class StringsWithCstring(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def return_input_string_type(input_string: str) -> str: ...

    @staticmethod
    def return_input_string(input_string: str) -> str: ...

