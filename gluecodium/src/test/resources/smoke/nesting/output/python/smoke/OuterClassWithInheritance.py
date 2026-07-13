

from smoke.ParentClass import ParentClass

class OuterClassWithInheritance(
    ParentClass):
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self, input: str) -> str:
        """"""
        return self._native.foo(input)

