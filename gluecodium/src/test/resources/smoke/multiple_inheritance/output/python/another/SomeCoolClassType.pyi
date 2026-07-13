


from _native_base import _NativeBase


class SomeCoolClassType(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_important_stuff(self):
        """"""
        return self._native.do_important_stuff()

