

from smoke.off.SomeStruct import SomeStruct

class NestedPackages:
    """"""

    def __init__(self, native):
        self._native = native


    def basic_method(self, input: SomeStruct) -> SomeStruct:
        """"""
        return self._native.basic_method(input)

