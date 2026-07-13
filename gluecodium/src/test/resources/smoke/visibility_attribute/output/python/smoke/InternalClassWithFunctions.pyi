



from _native_base import _NativeBase

import generated


class InternalClassWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo_bar(self):
        """"""
        return self._native.foo_bar()

    @staticmethod

    def make() -> InternalClassWithFunctions:
        """"""
        native_result = generated.InternalClassWithFunctions.make()
        return InternalClassWithFunctions(native_result)

    @staticmethod

    def make(foo: str) -> InternalClassWithFunctions:
        """"""
        native_result = generated.InternalClassWithFunctions.make(foo)
        return InternalClassWithFunctions(native_result)

