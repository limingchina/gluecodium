

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)


