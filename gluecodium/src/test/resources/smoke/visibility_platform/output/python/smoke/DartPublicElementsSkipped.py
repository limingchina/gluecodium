


class DartPublicElementsSkipped:
    """"""

    def __init__(self, native):
        self._native = native


    bool_field: bool


    string_field: str


    def foo(self):
        """"""
        return self._native.foo()

