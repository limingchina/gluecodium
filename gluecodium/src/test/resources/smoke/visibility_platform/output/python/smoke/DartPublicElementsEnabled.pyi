


from _native_base import _NativeBase


class DartPublicElementsEnabled(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    bool_field: bool


    string_field: str


    def foo(self):
        """"""
        return self._native.foo()

