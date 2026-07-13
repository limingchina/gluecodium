

from smoke.InternalNestedLambda import InternalNestedLambda

from _native_base import _NativeBase


class ClassWithInternalLambda(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def invoke_internal_lambda(self, lambda: InternalNestedLambda, value: str) -> bool:
        """"""
        return self._native.invoke_internal_lambda(lambda, value)

