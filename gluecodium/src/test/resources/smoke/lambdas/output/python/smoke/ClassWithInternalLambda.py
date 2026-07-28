

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional
from typing import Callable

from smoke.ClassWithInternalLambdaInternalNestedLambda import ClassWithInternalLambdaInternalNestedLambda

from _native_base import _NativeBase

import generated


class ClassWithInternalLambda(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def invoke_internal_lambda(lambda: Callable[[str], bool], value: str) -> bool:
        """"""
        return generated.smoke_ClassWithInternalLambda.invoke_internal_lambda(_unwrap(lambda, Callable[[str], bool]), _unwrap(value, str))

