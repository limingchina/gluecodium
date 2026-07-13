

from smoke.PublicStructWithInternalConstructors import PublicStructWithInternalConstructors

from _native_base import _NativeBase


class PublicStructWithInternalConstructors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    some_var: int


    def make(self) -> PublicStructWithInternalConstructors:
        """"""
        return self._native.make()

