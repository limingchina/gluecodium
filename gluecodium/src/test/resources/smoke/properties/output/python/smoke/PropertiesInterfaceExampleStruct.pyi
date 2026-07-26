

import typing


from _native_base import _NativeBase

import generated


class PropertiesInterfaceExampleStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PropertiesInterfaceExampleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PropertiesInterfaceExampleStruct(*[_unwrap(arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return _wrap(self._native.value, float)
    @value.setter
    def value(self, value: float):
      self._native.value = _unwrap(value, float)


