

from smoke.FooBarEnum import FooBarEnum

from _native_base import _NativeBase


class InternalEnumDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    public_field: FooBarEnum


    public_list_field: list[FooBarEnum]


    internal_field: FooBarEnum


    internal_list_field: list[FooBarEnum]

