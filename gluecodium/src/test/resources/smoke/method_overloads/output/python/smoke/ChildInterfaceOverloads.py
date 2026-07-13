

from smoke.ParentInterface import ParentInterface

class ChildInterfaceOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def bar(self, input: str):
        """"""
        return self._native.bar(input)

