


from _native_base import _NativeBase


class PlatformNamesListener(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def basic_method(self, basic_parameter: str):
        """"""
        return self._native.basic_method(basic_parameter)

