

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class ClassWithInternalLambda(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def invoke_internal_lambda(lambda_: Callable[[str], bool], value: str) -> bool:
        return _wrap(generated.smoke_ClassWithInternalLambda.invoke_internal_lambda(_unwrap(lambda_, Callable[[str], bool]), _unwrap(value, str)), bool)

    _InternalNestedLambda = Callable[[str], bool]
    
    

