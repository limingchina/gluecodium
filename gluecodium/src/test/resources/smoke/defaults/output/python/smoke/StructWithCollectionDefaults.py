

from __future__ import annotations



from _native_base import _NativeBase

import generated


class StructWithCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithCollectionDefaults(*args))


    @property
    def empty_list_field(self) -> list[str]:
        """"""
        return self._native.empty_list_field

    @empty_list_field.setter
    def empty_list_field(self, value: list[str]):
        self._native.empty_list_field = value



    @property
    def empty_map_field(self) -> dict[str, str]:
        """"""
        return self._native.empty_map_field

    @empty_map_field.setter
    def empty_map_field(self, value: dict[str, str]):
        self._native.empty_map_field = value



    @property
    def empty_set_field(self) -> set[str]:
        """"""
        return self._native.empty_set_field

    @empty_set_field.setter
    def empty_set_field(self, value: set[str]):
        self._native.empty_set_field = value



    @property
    def list_field(self) -> list[str]:
        """"""
        return self._native.list_field

    @list_field.setter
    def list_field(self, value: list[str]):
        self._native.list_field = value



    @property
    def map_field(self) -> dict[str, str]:
        """"""
        return self._native.map_field

    @map_field.setter
    def map_field(self, value: dict[str, str]):
        self._native.map_field = value



    @property
    def set_field(self) -> set[str]:
        """"""
        return self._native.set_field

    @set_field.setter
    def set_field(self, value: set[str]):
        self._native.set_field = value


