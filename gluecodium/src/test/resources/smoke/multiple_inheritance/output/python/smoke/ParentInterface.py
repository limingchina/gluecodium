

from another.SomeCoolClassType import SomeCoolClassType

class ParentInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_function(self):
        """"""
        return self._native.parent_function()


    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        """"""
        return self._native.some_function_that_uses_type_from_another_package(some_param)


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property


