

from __future__ import annotations



from _native_base import _NativeBase

import generated


class UseEnumOptionSet(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], UseEnumOptionSet):
            super().__init__(args[0])
        else:
            super().__init__(generated.UseEnumOptionSet(*args))


    @property
    def set_field(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field

    @set_field.setter
    def set_field(self, value: set[EnumOptionSet]):
        self._native.set_field = value



    @property
    def set_field_empty(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field_empty

    @set_field_empty.setter
    def set_field_empty(self, value: set[EnumOptionSet]):
        self._native.set_field_empty = value



    @property
    def set_field_value(self) -> set[EnumOptionSet]:
        """"""
        return self._native.set_field_value

    @set_field_value.setter
    def set_field_value(self, value: set[EnumOptionSet]):
        self._native.set_field_value = value


    @staticmethod

    def round_trip(input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        """"""
        native_result = generated.UseEnumOptionSet.round_trip(input)
        return set[EnumOptionSet](native_result)

