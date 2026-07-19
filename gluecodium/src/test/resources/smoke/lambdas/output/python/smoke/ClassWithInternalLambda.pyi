

from smoke.ClassWithInternalLambdaInternalNestedLambda import ClassWithInternalLambdaInternalNestedLambda

from _native_base import _NativeBase

import generated


class ClassWithInternalLambda(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def invoke_internal_lambda(lambda: ClassWithInternalLambdaInternalNestedLambda, value: str) -> bool:
        """"""
        return generated.ClassWithInternalLambda.invoke_internal_lambda(lambda._native, value)

