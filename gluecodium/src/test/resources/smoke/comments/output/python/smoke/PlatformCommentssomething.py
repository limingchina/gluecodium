

from __future__ import annotations



from _native_base import _NativeBase

import generated


class PlatformCommentssomething(_NativeBase):
    """This is a."""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PlatformCommentssomething):
            super().__init__(args[0])
        else:
            super().__init__(generated.PlatformCommentssomething(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nothing(self) -> str:
        """"""
        return self._native.nothing
    @nothing.setter
    def nothing(self, value: str):
      self._native.nothing = getattr(value, "_native", value)


