


from _native_base import _NativeBase


class UnderscorePackage(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def basic_method(self, input_string: str) -> str:
        """"""
        return self._native.basic_method(input_string)

