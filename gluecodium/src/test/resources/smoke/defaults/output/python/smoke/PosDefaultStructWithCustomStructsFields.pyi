

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults
from smoke.PosDefaultStructWithFieldUsingImmutableStruct import PosDefaultStructWithFieldUsingImmutableStruct
from smoke.SomeMutableCustomStructWithDefaults import SomeMutableCustomStructWithDefaults
from smoke.StructWithAllDefaults import StructWithAllDefaults
from smoke.StructWithNullableCollectionDefaults import StructWithNullableCollectionDefaults
from enum import Enum
import typing

class PosDefaultStructWithCustomStructsFields:

    const_ctor_field0: ImmutableStructWithDefaults

    const_ctor_field1: Optional[ImmutableStructWithDefaults]

    const_ctor_field2: list[str]

    const_ctor_field3: Optional[dict[str, str]]

    const_ctor_field4: int

    const_ctor_field5: float

    const_ctor_field6: Optional[ImmutableStructWithDefaults]

    const_ctor_field7: Optional[ImmutableStructWithDefaults]

    non_const_ctor_field0: StructWithAllDefaults

    non_const_ctor_field1: PosDefaultStructWithFieldUsingImmutableStruct

    non_const_ctor_field2: SomeMutableCustomStructWithDefaults

    non_const_ctor_field3: StructWithNullableCollectionDefaults

    non_const_ctor_field4: Optional[StructWithAllDefaults]

    non_const_ctor_field5: bytes

    non_const_ctor_field6: bytes

    non_const_ctor_field7: Optional[bytes]


