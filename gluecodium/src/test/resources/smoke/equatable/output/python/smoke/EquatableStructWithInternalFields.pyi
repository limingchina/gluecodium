



from _native_base import _NativeBase

import generated


class EquatableStructWithInternalFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], EquatableStructWithInternalFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.EquatableStructWithInternalFields(*args))


    @property
    def public_field(self) -> str:
        """"""
        return self._native.public_field

    @public_field.setter
    def public_field(self, value: str):
        self._native.public_field = value



    @property
    def internal_field(self) -> str:
        """"""
        return self._native.internal_field

    @internal_field.setter
    def internal_field(self, value: str):
        self._native.internal_field = value



    @property
    def internal_list_field(self) -> list[str]:
        """"""
        return self._native.internal_list_field

    @internal_list_field.setter
    def internal_list_field(self, value: list[str]):
        self._native.internal_list_field = value



    @property
    def internal_map_field(self) -> dict[str, str]:
        """"""
        return self._native.internal_map_field

    @internal_map_field.setter
    def internal_map_field(self, value: dict[str, str]):
        self._native.internal_map_field = value



    @property
    def internal_set_field(self) -> set[str]:
        """"""
        return self._native.internal_set_field

    @internal_set_field.setter
    def internal_set_field(self, value: set[str]):
        self._native.internal_set_field = value


