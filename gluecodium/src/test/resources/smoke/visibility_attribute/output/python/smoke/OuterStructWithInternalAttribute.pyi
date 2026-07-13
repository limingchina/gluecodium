

from smoke.StructNestedInInternalStruct import StructNestedInInternalStruct

from _native_base import _NativeBase


class OuterStructWithInternalAttribute(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    inner: StructNestedInInternalStruct

