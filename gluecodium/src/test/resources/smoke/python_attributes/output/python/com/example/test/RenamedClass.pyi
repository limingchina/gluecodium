


from _native_base import _NativeBase


class RenamedClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def internal_method(self) -> str:
        """"""
        return self._native.internal_method()


    def visible_method(self, param: int) -> str:
        """"""
        return self._native.visible_method(param)

