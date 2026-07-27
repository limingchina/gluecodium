

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class ListenersWithReturnValuesResultStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ListenersWithReturnValuesResultStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ListenersWithReturnValuesResultStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def result(self) -> float:
        """"""
        return _wrap(self._native.result, float)
    @result.setter
    def result(self, value: float):
      self._native.result = _unwrap(value, float)


