

from __future__ import annotations

from smoke.InternalNestedLambda import InternalNestedLambda


from _native_base import _NativeBase

import generated


class ClassWithInternalLambda(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def invoke_internal_lambda(lambda: InternalNestedLambda, value: str) -> bool:
        """"""
        return generated.ClassWithInternalLambda.invoke_internal_lambda(lambda._native, value)

