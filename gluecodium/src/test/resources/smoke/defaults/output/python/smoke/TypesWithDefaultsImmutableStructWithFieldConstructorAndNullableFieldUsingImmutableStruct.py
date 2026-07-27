

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


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


