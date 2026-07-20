

from __future__ import annotations

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsMutableStructWithCppAccessors(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsMutableStructWithCppAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsMutableStructWithCppAccessors(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def trivial_int_field(self) -> int:
        """"""
        return self._native.trivial_int_field
    @trivial_int_field.setter
    def trivial_int_field(self, value: int):
      self._native.trivial_int_field = getattr(value, "_native", value)



    @property
    def trivial_double_field(self) -> float:
        """"""
        return self._native.trivial_double_field
    @trivial_double_field.setter
    def trivial_double_field(self, value: float):
      self._native.trivial_double_field = getattr(value, "_native", value)



    @property
    def nontrivial_string_field(self) -> str:
        """"""
        return self._native.nontrivial_string_field
    @nontrivial_string_field.setter
    def nontrivial_string_field(self, value: str):
      self._native.nontrivial_string_field = getattr(value, "_native", value)



    @property
    def nontrivial_point_field(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.nontrivial_point_field)
    @nontrivial_point_field.setter
    def nontrivial_point_field(self, value: StructsPoint):
      self._native.nontrivial_point_field = getattr(value, "_native", value)



    @property
    def nontrivial_optional_point(self):
        """"""
        return Optional[StructsPoint](self._native.nontrivial_optional_point)
    @nontrivial_optional_point.setter
    def nontrivial_optional_point(self, value):
      self._native.nontrivial_optional_point = getattr(value, "_native", value)


