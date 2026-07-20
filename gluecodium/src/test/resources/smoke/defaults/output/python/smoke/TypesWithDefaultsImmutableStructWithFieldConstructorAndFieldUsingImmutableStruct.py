

from __future__ import annotations

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field1(self) -> TypesWithDefaultsSomeImmutableStructWithDefaults:
        """"""
        return TypesWithDefaultsSomeImmutableStructWithDefaults(self._native.some_field1)



    @property
    def some_field2(self) -> TypesWithDefaultsImmutableStructWithCollections:
        """"""
        return TypesWithDefaultsImmutableStructWithCollections(self._native.some_field2)



    @property
    def some_field(self) -> int:
        """"""
        return self._native.some_field



    @property
    def another_field(self) -> int:
        """"""
        return self._native.another_field


