


class InterfaceWithOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_method(self):
        """"""
        return self._native.parent_method()


    def parent_method(self, input: str):
        """"""
        return self._native.parent_method(input)

