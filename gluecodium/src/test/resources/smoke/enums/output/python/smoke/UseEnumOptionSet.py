

from __future__ import annotations



from _native_base import _NativeBase

import generated


class UseEnumOptionSet(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], UseEnumOptionSet):
            super().__init__(args[0])
        else:
            super().__init__(generated.UseEnumOptionSet(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def set_field(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field

    @set_field.setter
    def set_field(self, value: set[EnumOptionSet]):
      self._native.set_field = getattr(value, "_native", value)



    @property
    def set_field_empty(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field_empty

    @set_field_empty.setter
    def set_field_empty(self, value: set[EnumOptionSet]):
      self._native.set_field_empty = getattr(value, "_native", value)



    @property
    def set_field_value(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field_value

    @set_field_value.setter
    def set_field_value(self, value: set[EnumOptionSet]):
      self._native.set_field_value = getattr(value, "_native", value)


    @staticmethod
    def round_trip(input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        """"""
        return generated.UseEnumOptionSet.round_trip(input)

