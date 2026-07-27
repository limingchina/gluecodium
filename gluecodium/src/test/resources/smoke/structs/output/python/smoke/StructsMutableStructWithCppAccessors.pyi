

from smoke.StructsPoint import StructsPoint
import typing


from _native_base import _NativeBase

import generated


class StructsMutableStructWithCppAccessors(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsMutableStructWithCppAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsMutableStructWithCppAccessors(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def trivial_int_field(self) -> int:
        """"""
        return _wrap(self._native.trivial_int_field, int)
    @trivial_int_field.setter
    def trivial_int_field(self, value: int):
      self._native.trivial_int_field = _unwrap(value, int)



    @property
    def trivial_double_field(self) -> float:
        """"""
        return _wrap(self._native.trivial_double_field, float)
    @trivial_double_field.setter
    def trivial_double_field(self, value: float):
      self._native.trivial_double_field = _unwrap(value, float)



    @property
    def nontrivial_string_field(self) -> str:
        """"""
        return _wrap(self._native.nontrivial_string_field, str)
    @nontrivial_string_field.setter
    def nontrivial_string_field(self, value: str):
      self._native.nontrivial_string_field = _unwrap(value, str)



    @property
    def nontrivial_point_field(self) -> StructsPoint:
        """"""
        return _wrap(self._native.nontrivial_point_field, StructsPoint)
    @nontrivial_point_field.setter
    def nontrivial_point_field(self, value: StructsPoint):
      self._native.nontrivial_point_field = _unwrap(value, StructsPoint)



    @property
    def nontrivial_optional_point(self):
        """"""
        return _wrap(self._native.nontrivial_optional_point, Optional[StructsPoint])
    @nontrivial_optional_point.setter
    def nontrivial_optional_point(self, value):
      self._native.nontrivial_optional_point = _unwrap(value, Optional[StructsPoint])


