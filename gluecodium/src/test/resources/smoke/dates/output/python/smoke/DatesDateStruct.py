

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DatesDateStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DatesDateStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DatesDateStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def date_field(self) -> datetime.datetime:
        """"""
        return self._native.date_field
    @date_field.setter
    def date_field(self, value: datetime.datetime):
      self._native.date_field = getattr(value, "_native", value)



    @property
    def nullable_date_field(self):
        """"""
        return self._native.nullable_date_field
    @nullable_date_field.setter
    def nullable_date_field(self, value):
      self._native.nullable_date_field = getattr(value, "_native", value)


