

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class Rectangle(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Rectangle):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_Rectangle(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def left(self) -> int:
        """"""
        return _wrap(self._native.left, int)
    @left.setter
    def left(self, value: int):
      self._native.left = _unwrap(value, int)



    @property
    def top(self) -> int:
        """"""
        return _wrap(self._native.top, int)
    @top.setter
    def top(self, value: int):
      self._native.top = _unwrap(value, int)



    @property
    def width(self) -> int:
        """"""
        return _wrap(self._native.width, int)
    @width.setter
    def width(self, value: int):
      self._native.width = _unwrap(value, int)



    @property
    def height(self) -> int:
        """"""
        return _wrap(self._native.height, int)
    @height.setter
    def height(self, value: int):
      self._native.height = _unwrap(value, int)


