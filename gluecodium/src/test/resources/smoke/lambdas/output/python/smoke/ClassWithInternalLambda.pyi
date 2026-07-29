

from smoke.ClassWithInternalLambdaInternalNestedLambda import ClassWithInternalLambdaInternalNestedLambda
import typing
from typing import Callable

from _native_base import _NativeBase

import generated


class ClassWithInternalLambda(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def invoke_internal_lambda(lambda_: Callable[[str], bool], value: str) -> bool: ...

