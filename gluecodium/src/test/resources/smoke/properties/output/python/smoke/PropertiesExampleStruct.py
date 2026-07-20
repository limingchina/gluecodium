

from __future__ import annotations



from _native_base import _NativeBase

import generated


class PropertiesExampleStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PropertiesExampleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.PropertiesExampleStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return self._native.value
    @value.setter
    def value(self, value: float):
      self._native.value = getattr(value, "_native", value)


