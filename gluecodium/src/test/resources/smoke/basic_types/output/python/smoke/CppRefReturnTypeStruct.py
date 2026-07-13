


class CppRefReturnTypeStruct:
    """"""

    def __init__(self, native):
        self._native = native


    def string_ref(self) -> str:
        """"""
        return self._native.string_ref()

