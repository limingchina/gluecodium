


from _native_base import _NativeBase


class InternalClassWithStaticProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def foo_bar(self) -> str:
        """"""
        return self._native.foo_bar


