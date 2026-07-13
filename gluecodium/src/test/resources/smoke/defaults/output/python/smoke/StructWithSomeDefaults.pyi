



from _native_base import _NativeBase

import generated


class StructWithSomeDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithSomeDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithSomeDefaults(*args))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field

    @int_field.setter
    def int_field(self, value: int):
        self._native.int_field = value



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field

    @string_field.setter
    def string_field(self, value: str):
        self._native.string_field = value


