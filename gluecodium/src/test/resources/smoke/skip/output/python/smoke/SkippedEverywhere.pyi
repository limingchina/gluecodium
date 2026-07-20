

import typing


from _native_base import _NativeBase

import generated


class SkippedEverywhere(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkippedEverywhere):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkippedEverywhere(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nothing_to_see_here(self) -> str:
        """"""
        return self._native.nothing_to_see_here
    @nothing_to_see_here.setter
    def nothing_to_see_here(self, value: str):
      self._native.nothing_to_see_here = getattr(value, "_native", value)


    def use_map_in_dart(self, foo: dict[int, SkipTypesNotInDart]): ...

