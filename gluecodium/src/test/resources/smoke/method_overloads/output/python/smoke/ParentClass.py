


class ParentClass:
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self):
        """"""
        return self._native.foo()


    def foo(self, input: int):
        """"""
        return self._native.foo(input)


    def bar(self):
        """"""
        return self._native.bar()


    def baz(self):
        """"""
        return self._native.baz()

