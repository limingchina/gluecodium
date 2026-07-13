

from __future__ import annotations



from _native_base import _NativeBase

import generated


class Rectangle(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Rectangle):
            super().__init__(args[0])
        else:
            super().__init__(generated.Rectangle(*args))


    @property
    def left(self) -> int:
        """"""
        return self._native.left

    @left.setter
    def left(self, value: int):
        self._native.left = value



    @property
    def top(self) -> int:
        """"""
        return self._native.top

    @top.setter
    def top(self, value: int):
        self._native.top = value



    @property
    def width(self) -> int:
        """"""
        return self._native.width

    @width.setter
    def width(self, value: int):
        self._native.width = value



    @property
    def height(self) -> int:
        """"""
        return self._native.height

    @height.setter
    def height(self, value: int):
        self._native.height = value


