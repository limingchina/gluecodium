

from smoke.dict[str, int] import dict[str, int]
from smoke.list[str] import list[str]

from _native_base import _NativeBase


class DartInternalClassWithInternalTypedef(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def numbers(self) -> dict[str, int]:
        """"""
        return self._native.numbers



    @property
    def labels(self) -> list[str]:
        """"""
        return self._native.labels


