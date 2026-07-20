

import typing

from _native_base import _NativeBase

import generated


class AsyncWithSkips(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    @staticmethod
    def make_shared_instance(android_context: str): ...

    @typing.overload
    @staticmethod
    def make_shared_instance(): ...

