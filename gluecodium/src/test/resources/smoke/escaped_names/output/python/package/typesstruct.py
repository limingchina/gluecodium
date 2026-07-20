

from __future__ import annotations

from package.typesenum import typesenum


from _native_base import _NativeBase

import generated


class typesstruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.typesstruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.typesstruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def null(self) -> typesenum:
        """"""
        return typesenum(self._native.null)
    @null.setter
    def null(self, value: typesenum):
      self._native.null = getattr(value, "_native", value)


