

import typing


from _native_base import _NativeBase

import generated


class NameRulesExampleStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.NameRulesExampleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.NameRulesExampleStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return self._native.value
    @value.setter
    def value(self, value: float):
      self._native.value = getattr(value, "_native", value)



    @property
    def int_value(self) -> list[int]:
        """"""
        return self._native.int_value
    @int_value.setter
    def int_value(self, value: list[int]):
      self._native.int_value = getattr(value, "_native", value)


