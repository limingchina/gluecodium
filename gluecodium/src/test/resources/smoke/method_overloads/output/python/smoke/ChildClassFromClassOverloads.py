

from smoke.ParentClass import ParentClass

class ChildClassFromClassOverloads(
    ParentClass):
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def foo(self, input: float):
        """"""
        return self._native.foo(input)


    def bar(self, input: str):
        """"""
        return self._native.bar(input)


    def bar(self, input: float):
        """"""
        return self._native.bar(input)

