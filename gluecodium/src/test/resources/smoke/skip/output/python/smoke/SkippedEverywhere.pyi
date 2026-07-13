



from _native_base import _NativeBase

import generated


class SkippedEverywhere(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SkippedEverywhere):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkippedEverywhere(*args))


    @property
    def nothing_to_see_here(self) -> str:
        """"""
        return self._native.nothing_to_see_here

    @nothing_to_see_here.setter
    def nothing_to_see_here(self, value: str):
        self._native.nothing_to_see_here = value



    def use_map_in_dart(self, foo: dict[int, NotInDart]):
        """"""
        return self._native.use_map_in_dart(foo)

