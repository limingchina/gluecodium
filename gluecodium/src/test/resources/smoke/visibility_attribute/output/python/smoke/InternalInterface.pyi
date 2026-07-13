


from _native_base import _NativeBase


class InternalInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @property
    def some_property_of_internal_interface(self) -> str:
        """"""
        return self._native.some_property_of_internal_interface


