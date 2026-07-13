


class ExternalClass:
    """"""

    def __init__(self, native):
        self._native = native


    def some_method(self, some_parameter: int):
        """"""
        return self._native.some_method(some_parameter)


    @property
    def some_property(self) -> str:
        """"""
        return self._native.some_property


