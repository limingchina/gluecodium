

from enum import Enum
import typing
from typing import Callable

class ClassWithInternalLambda:

    @staticmethod
    def invoke_internal_lambda(lambda_: Callable[[str], bool], value: str) -> bool:
        ...

    _InternalNestedLambda = Callable[[str], bool]
    
    

