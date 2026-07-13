

from smoke.PI import PI

class AttributesClass:
    """"""

    def __init__(self, native):
        self._native = native


    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop


