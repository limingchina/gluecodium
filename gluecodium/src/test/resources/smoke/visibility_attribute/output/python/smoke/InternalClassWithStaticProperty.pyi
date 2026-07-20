

import typing

from _native_base import _NativeBase

import generated


class InternalClassWithStaticProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @staticmethod
    def foo_bar() -> str:
        """"""
        return generated.InternalClassWithStaticProperty.foo_bar()

