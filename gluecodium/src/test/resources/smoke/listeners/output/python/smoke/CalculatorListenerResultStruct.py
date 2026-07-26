

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class CalculatorListenerResultStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_CalculatorListenerResultStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_CalculatorListenerResultStruct(*[_unwrap(arg) for arg in args]))


    @property
    def result(self) -> float:
        """"""
        return _wrap(self._native.result, float)
    @result.setter
    def result(self, value: float):
      self._native.result = _unwrap(value, float)


