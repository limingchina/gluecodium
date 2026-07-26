

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults
import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field1(self):
        """"""
        return _wrap(self._native.some_field1, Optional[TypesWithDefaultsSomeImmutableStructWithDefaults])



    @property
    def some_field2(self):
        """"""
        return _wrap(self._native.some_field2, Optional[TypesWithDefaultsImmutableStructWithCollections])


