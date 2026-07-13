

from __future__ import annotations

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults
from smoke.PosDefaultStructWithFieldUsingImmutableStruct import PosDefaultStructWithFieldUsingImmutableStruct
from smoke.SomeMutableCustomStructWithDefaults import SomeMutableCustomStructWithDefaults
from smoke.StructWithAllDefaults import StructWithAllDefaults
from smoke.StructWithNullableCollectionDefaults import StructWithNullableCollectionDefaults


from _native_base import _NativeBase

import generated


class PosDefaultStructWithCustomStructsFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], PosDefaultStructWithCustomStructsFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.PosDefaultStructWithCustomStructsFields(*args))


    @property
    def const_ctor_field0(self) -> ImmutableStructWithDefaults:
        """"""
        return self._native.const_ctor_field0

    @const_ctor_field0.setter
    def const_ctor_field0(self, value: ImmutableStructWithDefaults):
        self._native.const_ctor_field0 = value



    @property
    def const_ctor_field1(self):
        """"""
        return self._native.const_ctor_field1

    @const_ctor_field1.setter
    def const_ctor_field1(self, value):
        self._native.const_ctor_field1 = value



    @property
    def const_ctor_field2(self) -> list[str]:
        """"""
        return self._native.const_ctor_field2

    @const_ctor_field2.setter
    def const_ctor_field2(self, value: list[str]):
        self._native.const_ctor_field2 = value



    @property
    def const_ctor_field3(self):
        """"""
        return self._native.const_ctor_field3

    @const_ctor_field3.setter
    def const_ctor_field3(self, value):
        self._native.const_ctor_field3 = value



    @property
    def const_ctor_field4(self) -> int:
        """"""
        return self._native.const_ctor_field4

    @const_ctor_field4.setter
    def const_ctor_field4(self, value: int):
        self._native.const_ctor_field4 = value



    @property
    def const_ctor_field5(self) -> float:
        """"""
        return self._native.const_ctor_field5

    @const_ctor_field5.setter
    def const_ctor_field5(self, value: float):
        self._native.const_ctor_field5 = value



    @property
    def const_ctor_field6(self):
        """"""
        return self._native.const_ctor_field6

    @const_ctor_field6.setter
    def const_ctor_field6(self, value):
        self._native.const_ctor_field6 = value



    @property
    def const_ctor_field7(self):
        """"""
        return self._native.const_ctor_field7

    @const_ctor_field7.setter
    def const_ctor_field7(self, value):
        self._native.const_ctor_field7 = value



    @property
    def non_const_ctor_field0(self) -> StructWithAllDefaults:
        """"""
        return self._native.non_const_ctor_field0

    @non_const_ctor_field0.setter
    def non_const_ctor_field0(self, value: StructWithAllDefaults):
        self._native.non_const_ctor_field0 = value



    @property
    def non_const_ctor_field1(self) -> PosDefaultStructWithFieldUsingImmutableStruct:
        """"""
        return self._native.non_const_ctor_field1

    @non_const_ctor_field1.setter
    def non_const_ctor_field1(self, value: PosDefaultStructWithFieldUsingImmutableStruct):
        self._native.non_const_ctor_field1 = value



    @property
    def non_const_ctor_field2(self) -> SomeMutableCustomStructWithDefaults:
        """"""
        return self._native.non_const_ctor_field2

    @non_const_ctor_field2.setter
    def non_const_ctor_field2(self, value: SomeMutableCustomStructWithDefaults):
        self._native.non_const_ctor_field2 = value



    @property
    def non_const_ctor_field3(self) -> StructWithNullableCollectionDefaults:
        """"""
        return self._native.non_const_ctor_field3

    @non_const_ctor_field3.setter
    def non_const_ctor_field3(self, value: StructWithNullableCollectionDefaults):
        self._native.non_const_ctor_field3 = value



    @property
    def non_const_ctor_field4(self):
        """"""
        return self._native.non_const_ctor_field4

    @non_const_ctor_field4.setter
    def non_const_ctor_field4(self, value):
        self._native.non_const_ctor_field4 = value



    @property
    def non_const_ctor_field5(self) -> bytes:
        """"""
        return self._native.non_const_ctor_field5

    @non_const_ctor_field5.setter
    def non_const_ctor_field5(self, value: bytes):
        self._native.non_const_ctor_field5 = value



    @property
    def non_const_ctor_field6(self) -> bytes:
        """"""
        return self._native.non_const_ctor_field6

    @non_const_ctor_field6.setter
    def non_const_ctor_field6(self, value: bytes):
        self._native.non_const_ctor_field6 = value



    @property
    def non_const_ctor_field7(self):
        """"""
        return self._native.non_const_ctor_field7

    @non_const_ctor_field7.setter
    def non_const_ctor_field7(self, value):
        self._native.non_const_ctor_field7 = value


