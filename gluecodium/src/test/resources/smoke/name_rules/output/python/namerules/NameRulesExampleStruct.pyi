

import typing


from _native_base import _NativeBase

import generated


class NameRulesExampleStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.namerules_NameRulesExampleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.namerules_NameRulesExampleStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def value(self) -> float:
        """"""
        return _wrap(self._native.value, float)
    @value.setter
    def value(self, value: float):
      self._native.value = _unwrap(value, float)



    @property
    def int_value(self) -> list[int]:
        """"""
        return _wrap(self._native.int_value, list[int])
    @int_value.setter
    def int_value(self, value: list[int]):
      self._native.int_value = _unwrap(value, list[int])


