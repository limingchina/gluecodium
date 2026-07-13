

from smoke.FcStruct import FcStruct

from _native_base import _NativeBase


class DefaultsWithFcStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    struct_field: FcStruct

