

from smoke.ExternalEnum import ExternalEnum

from _native_base import _NativeBase


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_external_enum(self, input: ExternalEnum):
        """"""
        return self._native.method_with_external_enum(input)

