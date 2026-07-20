

import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithFieldConstructorAndCollections(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndCollections):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndCollections(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nullable_list_field(self):
        """"""
        return self._native.nullable_list_field



    @property
    def empty_list_field(self) -> list[int]:
        """"""
        return self._native.empty_list_field



    @property
    def values_list_field(self) -> list[int]:
        """"""
        return self._native.values_list_field



    @property
    def nullable_map_field(self):
        """"""
        return self._native.nullable_map_field



    @property
    def empty_map_field(self) -> dict[int, str]:
        """"""
        return self._native.empty_map_field



    @property
    def values_map_field(self) -> dict[int, str]:
        """"""
        return self._native.values_map_field



    @property
    def nullable_set_field(self):
        """"""
        return self._native.nullable_set_field



    @property
    def empty_set_field(self) -> set[str]:
        """"""
        return self._native.empty_set_field



    @property
    def values_set_field(self) -> set[str]:
        """"""
        return self._native.values_set_field



    @property
    def some_field(self) -> int:
        """"""
        return self._native.some_field



    @property
    def another_field(self) -> int:
        """"""
        return self._native.another_field


