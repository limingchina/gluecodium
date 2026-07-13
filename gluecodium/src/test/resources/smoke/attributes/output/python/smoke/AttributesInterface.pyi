

from smoke.PI import PI


from _native_base import _NativeBase

import generated


class AttributesInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, AttributesInterface):
            super().__init__(native)
        else:
            super().__init__(generated.AttributesInterface())


    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop

    @prop.setter
    def prop(self, value: str):
        self._native.prop = value

