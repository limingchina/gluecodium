

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults
from smoke.PosDefaultStructWithFieldUsingImmutableStruct import PosDefaultStructWithFieldUsingImmutableStruct
from smoke.SomeMutableCustomStructWithDefaults import SomeMutableCustomStructWithDefaults
from smoke.StructWithAllDefaults import StructWithAllDefaults
from smoke.StructWithNullableCollectionDefaults import StructWithNullableCollectionDefaults


from _native_base import _NativeBase

import generated


class PosDefaultStructWithCustomStructsFields(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PosDefaultStructWithCustomStructsFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PosDefaultStructWithCustomStructsFields(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def const_ctor_field0(self) -> ImmutableStructWithDefaults:
        return _wrap(self._native.const_ctor_field0, ImmutableStructWithDefaults)


    @property
    def const_ctor_field1(self):
        return _wrap(self._native.const_ctor_field1, Optional[ImmutableStructWithDefaults])


    @property
    def const_ctor_field2(self) -> list[str]:
        return _wrap(self._native.const_ctor_field2, list[str])
    @const_ctor_field2.setter
    def const_ctor_field2(self, value: list[str]):
      self._native.const_ctor_field2 = _unwrap(value, list[str])


    @property
    def const_ctor_field3(self):
        return _wrap(self._native.const_ctor_field3, Optional[dict[str, str]])
    @const_ctor_field3.setter
    def const_ctor_field3(self, value):
      self._native.const_ctor_field3 = _unwrap(value, Optional[dict[str, str]])


    @property
    def const_ctor_field4(self) -> int:
        return _wrap(self._native.const_ctor_field4, int)
    @const_ctor_field4.setter
    def const_ctor_field4(self, value: int):
      self._native.const_ctor_field4 = _unwrap(value, int)


    @property
    def const_ctor_field5(self) -> float:
        return _wrap(self._native.const_ctor_field5, float)
    @const_ctor_field5.setter
    def const_ctor_field5(self, value: float):
      self._native.const_ctor_field5 = _unwrap(value, float)


    @property
    def const_ctor_field6(self):
        return _wrap(self._native.const_ctor_field6, Optional[ImmutableStructWithDefaults])


    @property
    def const_ctor_field7(self):
        return _wrap(self._native.const_ctor_field7, Optional[ImmutableStructWithDefaults])


    @property
    def non_const_ctor_field0(self) -> StructWithAllDefaults:
        return _wrap(self._native.non_const_ctor_field0, StructWithAllDefaults)
    @non_const_ctor_field0.setter
    def non_const_ctor_field0(self, value: StructWithAllDefaults):
      self._native.non_const_ctor_field0 = _unwrap(value, StructWithAllDefaults)


    @property
    def non_const_ctor_field1(self) -> PosDefaultStructWithFieldUsingImmutableStruct:
        return _wrap(self._native.non_const_ctor_field1, PosDefaultStructWithFieldUsingImmutableStruct)


    @property
    def non_const_ctor_field2(self) -> SomeMutableCustomStructWithDefaults:
        return _wrap(self._native.non_const_ctor_field2, SomeMutableCustomStructWithDefaults)
    @non_const_ctor_field2.setter
    def non_const_ctor_field2(self, value: SomeMutableCustomStructWithDefaults):
      self._native.non_const_ctor_field2 = _unwrap(value, SomeMutableCustomStructWithDefaults)


    @property
    def non_const_ctor_field3(self) -> StructWithNullableCollectionDefaults:
        return _wrap(self._native.non_const_ctor_field3, StructWithNullableCollectionDefaults)
    @non_const_ctor_field3.setter
    def non_const_ctor_field3(self, value: StructWithNullableCollectionDefaults):
      self._native.non_const_ctor_field3 = _unwrap(value, StructWithNullableCollectionDefaults)


    @property
    def non_const_ctor_field4(self):
        return _wrap(self._native.non_const_ctor_field4, Optional[StructWithAllDefaults])
    @non_const_ctor_field4.setter
    def non_const_ctor_field4(self, value):
      self._native.non_const_ctor_field4 = _unwrap(value, Optional[StructWithAllDefaults])


    @property
    def non_const_ctor_field5(self) -> bytes:
        return _wrap(self._native.non_const_ctor_field5, bytes)
    @non_const_ctor_field5.setter
    def non_const_ctor_field5(self, value: bytes):
      self._native.non_const_ctor_field5 = _unwrap(value, bytes)


    @property
    def non_const_ctor_field6(self) -> bytes:
        return _wrap(self._native.non_const_ctor_field6, bytes)
    @non_const_ctor_field6.setter
    def non_const_ctor_field6(self, value: bytes):
      self._native.non_const_ctor_field6 = _unwrap(value, bytes)


    @property
    def non_const_ctor_field7(self):
        return _wrap(self._native.non_const_ctor_field7, Optional[bytes])
    @non_const_ctor_field7.setter
    def non_const_ctor_field7(self, value):
      self._native.non_const_ctor_field7 = _unwrap(value, Optional[bytes])


