

import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithCollections(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithCollections):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithCollections(*[_unwrap(arg) for arg in args]))


    @property
    def nullable_list_field(self):
        """"""
        return _wrap(self._native.nullable_list_field, Optional[list[int]])



    @property
    def empty_list_field(self) -> list[int]:
        """"""
        return _wrap(self._native.empty_list_field, list[int])



    @property
    def values_list_field(self) -> list[int]:
        """"""
        return _wrap(self._native.values_list_field, list[int])



    @property
    def nullable_map_field(self):
        """"""
        return _wrap(self._native.nullable_map_field, Optional[dict[int, str]])



    @property
    def empty_map_field(self) -> dict[int, str]:
        """"""
        return _wrap(self._native.empty_map_field, dict[int, str])



    @property
    def values_map_field(self) -> dict[int, str]:
        """"""
        return _wrap(self._native.values_map_field, dict[int, str])



    @property
    def nullable_set_field(self):
        """"""
        return _wrap(self._native.nullable_set_field, Optional[set[str]])



    @property
    def empty_set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.empty_set_field, set[str])



    @property
    def values_set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.values_set_field, set[str])


