

from smoke.PI import PI

class AttributesStruct:
    """"""

    def __init__(self, native):
        self._native = native


    field: str


    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)

