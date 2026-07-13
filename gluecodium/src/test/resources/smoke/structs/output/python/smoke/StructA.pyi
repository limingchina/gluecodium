



from _native_base import _NativeBase

import generated


class StructA(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructA):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructA(*args))


    @property
    def field(self) -> list[StructB]:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: list[StructB]):
        self._native.field = value


