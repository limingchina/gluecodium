


from _native_base import _NativeBase


class InterfaceWithOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_method(self):
        """"""
        return self._native.parent_method()


    def parent_method(self, input: str):
        """"""
        return self._native.parent_method(input)

