



from _native_base import _NativeBase

import generated


class StructB(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructB):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructB(*args))


    @property
    def field(self) -> list[StructA]:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: list[StructA]):
        self._native.field = value


