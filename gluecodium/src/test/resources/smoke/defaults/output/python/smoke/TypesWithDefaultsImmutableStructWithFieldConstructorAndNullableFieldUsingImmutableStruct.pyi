

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults
import typing

class TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct:

    some_field1: Optional[TypesWithDefaultsSomeImmutableStructWithDefaults]

    some_field2: Optional[TypesWithDefaultsImmutableStructWithCollections]

    some_field: int

    another_field: int

