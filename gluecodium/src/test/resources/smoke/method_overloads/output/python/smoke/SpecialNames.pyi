

import typing

from _native_base import _NativeBase

import generated


class SpecialNames(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def create(self): ...

    def release(self): ...

    def create_proxy(self): ...

    def _uppercase(self): ...

    @staticmethod
    def make(result: str) -> SpecialNames: ...

