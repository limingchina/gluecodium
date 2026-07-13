

from smoke.FooBarEnum import FooBarEnum


from _native_base import _NativeBase

import generated


class InternalEnumDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], InternalEnumDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.InternalEnumDefaults(*args))


    @property
    def public_field(self) -> FooBarEnum:
        """"""
        return self._native.public_field

    @public_field.setter
    def public_field(self, value: FooBarEnum):
        self._native.public_field = value



    @property
    def public_list_field(self) -> list[FooBarEnum]:
        """"""
        return self._native.public_list_field

    @public_list_field.setter
    def public_list_field(self, value: list[FooBarEnum]):
        self._native.public_list_field = value



    @property
    def internal_field(self) -> FooBarEnum:
        """"""
        return self._native.internal_field

    @internal_field.setter
    def internal_field(self, value: FooBarEnum):
        self._native.internal_field = value



    @property
    def internal_list_field(self) -> list[FooBarEnum]:
        """"""
        return self._native.internal_list_field

    @internal_list_field.setter
    def internal_list_field(self, value: list[FooBarEnum]):
        self._native.internal_list_field = value


