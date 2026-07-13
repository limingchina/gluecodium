


class Locales:
    """"""

    def __init__(self, native):
        self._native = native


    def locale_method(self, input: str) -> str:
        """"""
        return self._native.locale_method(input)


    @property
    def locale_property(self) -> str:
        """"""
        return self._native.locale_property


