

from package.typesenum import typesenum
import typing


from _native_base import _NativeBase

import generated


class typesstruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.package_typesstruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.package_typesstruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def null(self) -> typesenum:
        """"""
        return _wrap(self._native.null, typesenum)
    @null.setter
    def null(self, value: typesenum):
      self._native.null = _unwrap(value, typesenum)


