

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
        native_result = generated.ClassWithInternalLambda.invoke_internal_lambda(lambda, value)
        return bool(native_result)

