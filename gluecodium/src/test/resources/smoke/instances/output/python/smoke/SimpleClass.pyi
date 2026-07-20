

import typing

from _native_base import _NativeBase

import generated


class SimpleClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def get_string_value(self) -> str: ...

    def use_simple_class(self, input: SimpleClass) -> SimpleClass: ...

