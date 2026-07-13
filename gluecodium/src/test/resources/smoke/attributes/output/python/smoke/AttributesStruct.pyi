

from smoke.PI import PI


from _native_base import _NativeBase

import generated


class AttributesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], AttributesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.AttributesStruct(*args))


    @property
    def field(self) -> str:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: str):
        self._native.field = value



    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)

