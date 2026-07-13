


class RenamedClass:
    """"""

    def __init__(self, native):
        self._native = native


    def internal_method(self) -> str:
        """"""
        return self._native.internal_method()


    def visible_method(self, param: int) -> str:
        """"""
        return self._native.visible_method(param)

