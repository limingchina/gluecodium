

from smoke.SomethingEnum import SomethingEnum


from _native_base import _NativeBase

import generated


class StructWithPosEnums(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithPosEnums):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithPosEnums(*args))


    @property
    def first_field(self) -> SomethingEnum:
        """"""
        return self._native.first_field

    @first_field.setter
    def first_field(self, value: SomethingEnum):
        self._native.first_field = value



    @property
    def explicit_field(self) -> SomethingEnum:
        """"""
        return self._native.explicit_field

    @explicit_field.setter
    def explicit_field(self, value: SomethingEnum):
        self._native.explicit_field = value



    @property
    def last_field(self) -> SomethingEnum:
        """"""
        return self._native.last_field

    @last_field.setter
    def last_field(self, value: SomethingEnum):
        self._native.last_field = value



FIRST_CONSTANT = SomethingEnum.REALLY_FIRST

