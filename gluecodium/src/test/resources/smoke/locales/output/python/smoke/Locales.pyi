


from _native_base import _NativeBase


class Locales(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def locale_method(self, input: str) -> str:
        """"""
        return self._native.locale_method(input)


    @property
    def locale_property(self) -> str:
        """"""
        return self._native.locale_property


