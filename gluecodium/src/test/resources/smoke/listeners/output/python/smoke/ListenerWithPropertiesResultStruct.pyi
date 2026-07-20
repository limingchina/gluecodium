

import typing


from _native_base import _NativeBase

import generated


class ListenerWithPropertiesResultStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ListenerWithPropertiesResultStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.ListenerWithPropertiesResultStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def result(self) -> float:
        """"""
        return self._native.result
    @result.setter
    def result(self, value: float):
      self._native.result = getattr(value, "_native", value)


