

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
        if len(args) == 1 and isinstance(args[0], generated.PosDefaultStructWithCustomStructsFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.PosDefaultStructWithCustomStructsFields(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def const_ctor_field0(self) -> ImmutableStructWithDefaults:
        """"""
        return ImmutableStructWithDefaults(self._native.const_ctor_field0)



    @property
    def const_ctor_field1(self):
        """"""
        return Optional[ImmutableStructWithDefaults](self._native.const_ctor_field1)



    @property
    def const_ctor_field2(self) -> list[str]:
        """"""
        return self._native.const_ctor_field2
    @const_ctor_field2.setter
    def const_ctor_field2(self, value: list[str]):
      self._native.const_ctor_field2 = getattr(value, "_native", value)



    @property
    def const_ctor_field3(self):
        """"""
        return self._native.const_ctor_field3
    @const_ctor_field3.setter
    def const_ctor_field3(self, value):
      self._native.const_ctor_field3 = getattr(value, "_native", value)



    @property
    def const_ctor_field4(self) -> int:
        """"""
        return self._native.const_ctor_field4
    @const_ctor_field4.setter
    def const_ctor_field4(self, value: int):
      self._native.const_ctor_field4 = getattr(value, "_native", value)



    @property
    def const_ctor_field5(self) -> float:
        """"""
        return self._native.const_ctor_field5
    @const_ctor_field5.setter
    def const_ctor_field5(self, value: float):
      self._native.const_ctor_field5 = getattr(value, "_native", value)



    @property
    def const_ctor_field6(self):
        """"""
        return Optional[ImmutableStructWithDefaults](self._native.const_ctor_field6)



    @property
    def const_ctor_field7(self):
        """"""
        return Optional[ImmutableStructWithDefaults](self._native.const_ctor_field7)



    @property
    def non_const_ctor_field0(self) -> StructWithAllDefaults:
        """"""
        return StructWithAllDefaults(self._native.non_const_ctor_field0)
    @non_const_ctor_field0.setter
    def non_const_ctor_field0(self, value: StructWithAllDefaults):
      self._native.non_const_ctor_field0 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field1(self) -> PosDefaultStructWithFieldUsingImmutableStruct:
        """"""
        return PosDefaultStructWithFieldUsingImmutableStruct(self._native.non_const_ctor_field1)



    @property
    def non_const_ctor_field2(self) -> SomeMutableCustomStructWithDefaults:
        """"""
        return SomeMutableCustomStructWithDefaults(self._native.non_const_ctor_field2)
    @non_const_ctor_field2.setter
    def non_const_ctor_field2(self, value: SomeMutableCustomStructWithDefaults):
      self._native.non_const_ctor_field2 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field3(self) -> StructWithNullableCollectionDefaults:
        """"""
        return StructWithNullableCollectionDefaults(self._native.non_const_ctor_field3)
    @non_const_ctor_field3.setter
    def non_const_ctor_field3(self, value: StructWithNullableCollectionDefaults):
      self._native.non_const_ctor_field3 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field4(self):
        """"""
        return Optional[StructWithAllDefaults](self._native.non_const_ctor_field4)
    @non_const_ctor_field4.setter
    def non_const_ctor_field4(self, value):
      self._native.non_const_ctor_field4 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field5(self) -> bytes:
        """"""
        return self._native.non_const_ctor_field5
    @non_const_ctor_field5.setter
    def non_const_ctor_field5(self, value: bytes):
      self._native.non_const_ctor_field5 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field6(self) -> bytes:
        """"""
        return self._native.non_const_ctor_field6
    @non_const_ctor_field6.setter
    def non_const_ctor_field6(self, value: bytes):
      self._native.non_const_ctor_field6 = getattr(value, "_native", value)



    @property
    def non_const_ctor_field7(self):
        """"""
        return self._native.non_const_ctor_field7
    @non_const_ctor_field7.setter
    def non_const_ctor_field7(self, value):
      self._native.non_const_ctor_field7 = getattr(value, "_native", value)


