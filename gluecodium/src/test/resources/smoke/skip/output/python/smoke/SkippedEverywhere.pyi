

from smoke.SkipTypesNotInDart import SkipTypesNotInDart
import typing


from _native_base import _NativeBase

import generated


class SkippedEverywhere(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_SkippedEverywhere):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SkippedEverywhere(*[_unwrap(arg) for arg in args]))


    @property
    def nothing_to_see_here(self) -> str:
        """"""
        return _wrap(self._native.nothing_to_see_here, str)
    @nothing_to_see_here.setter
    def nothing_to_see_here(self, value: str):
      self._native.nothing_to_see_here = _unwrap(value, str)


    def use_map_in_dart(self, foo: dict[int, SkipTypesNotInDart]): ...

