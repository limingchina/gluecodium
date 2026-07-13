



from _native_base import _NativeBase

import generated


class ParentClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


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

