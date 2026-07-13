


from _native_base import _NativeBase


class SkippedEverywhere(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    nothing_to_see_here: str


    def use_map_in_dart(self, foo: dict[int, NotInDart]):
        """"""
        return self._native.use_map_in_dart(foo)

