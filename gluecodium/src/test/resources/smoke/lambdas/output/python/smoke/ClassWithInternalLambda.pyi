

from smoke.ClassWithInternalLambdaInternalNestedLambda import ClassWithInternalLambdaInternalNestedLambda
import typing
from typing import Callable

class ClassWithInternalLambda:

    @staticmethod
    def invoke_internal_lambda(lambda_: Callable[[str], bool], value: str) -> bool:
        ...

