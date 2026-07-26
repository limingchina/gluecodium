

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field1(self) -> TypesWithDefaultsSomeImmutableStructWithDefaults:
        """"""
        return _wrap(self._native.some_field1, TypesWithDefaultsSomeImmutableStructWithDefaults)



    @property
    def some_field2(self) -> TypesWithDefaultsImmutableStructWithCollections:
        """"""
        return _wrap(self._native.some_field2, TypesWithDefaultsImmutableStructWithCollections)


