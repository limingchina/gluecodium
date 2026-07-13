


from _native_base import _NativeBase


class SkipTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def use_list_in_dart(self) -> list[NotInDart]:
        """"""
        return self._native.use_list_in_dart()

