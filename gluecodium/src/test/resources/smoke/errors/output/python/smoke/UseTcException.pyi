

from smoke.SomeError import SomeError
from smoke.SomeTypeCollectionError import SomeTypeCollectionError

from _native_base import _NativeBase


class UseTcException(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_nothing(self):
        """"""
        return self._native.do_nothing()

