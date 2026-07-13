

from smoke.ParentClass import ParentClass

class ForwardDeclarationBug(
    ParentClass):
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self, bar: ParentClass):
        """"""
        return self._native.foo(bar)

