

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ParentClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_fun(self):
        """"""
        return self._native.parent_fun()


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property

    @parent_property.setter
    def parent_property(self, value: str):
        self._native.parent_property = value

