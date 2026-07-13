

from smoke.FooBarEnum import FooBarEnum

class InternalEnumDefaults:
    """"""

    def __init__(self, native):
        self._native = native


    public_field: FooBarEnum


    public_list_field: list[FooBarEnum]


    internal_field: FooBarEnum


    internal_list_field: list[FooBarEnum]

