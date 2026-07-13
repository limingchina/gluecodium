



from _native_base import _NativeBase

import generated


class StructWithMap(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithMap):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithMap(*args))


    @property
    def field(self) -> dict[str, StructWithMap]:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: dict[str, StructWithMap]):
        self._native.field = value


