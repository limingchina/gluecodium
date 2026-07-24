

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field1(self):
        """"""
        return _wrap(self._native.some_field1, Optional[TypesWithDefaultsSomeImmutableStructWithDefaults])



    @property
    def some_field2(self):
        """"""
        return _wrap(self._native.some_field2, Optional[TypesWithDefaultsImmutableStructWithCollections])



    @property
    def some_field(self) -> int:
        """"""
        return _wrap(self._native.some_field, int)



    @property
    def another_field(self) -> int:
        """"""
        return _wrap(self._native.another_field, int)


