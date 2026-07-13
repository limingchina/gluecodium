


from _native_base import _NativeBase


class ParentInterfaceWithBool(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def root_method(self, input1: bool):
        """"""
        return self._native.root_method(input1)

