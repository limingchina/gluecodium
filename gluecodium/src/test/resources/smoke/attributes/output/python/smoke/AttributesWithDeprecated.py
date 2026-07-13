

from smoke.PI import PI

class AttributesWithDeprecated:
    """"""

    def __init__(self, native):
        self._native = native


    def very_fun(self):
        """"""
        return self._native.very_fun()


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop


