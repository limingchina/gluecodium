


class InternalInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @property
    def some_property_of_internal_interface(self) -> str:
        """"""
        return self._native.some_property_of_internal_interface


