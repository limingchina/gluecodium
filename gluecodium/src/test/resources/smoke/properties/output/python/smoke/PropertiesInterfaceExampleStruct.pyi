

import typing


from _native_base import _NativeBase

import generated


class PropertiesInterfaceExampleStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PropertiesInterfaceExampleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.PropertiesInterfaceExampleStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return self._native.value
    @value.setter
    def value(self, value: float):
      self._native.value = getattr(value, "_native", value)


