

from __future__ import annotations

from smoke.ImmutableStructNoClash import ImmutableStructNoClash


from _native_base import _NativeBase

import generated


class MutableStructImmutableFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], MutableStructImmutableFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.MutableStructImmutableFields(*args))


    @property
    def struct_field(self) -> ImmutableStructNoClash:
        """"""
        return self._native.struct_field

    @struct_field.setter
    def struct_field(self, value: ImmutableStructNoClash):
        self._native.struct_field = value



    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field

    @int_field.setter
    def int_field(self, value: int):
        self._native.int_field = value



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field

    @bool_field.setter
    def bool_field(self, value: bool):
        self._native.bool_field = value


