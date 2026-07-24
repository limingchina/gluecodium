

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda import ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda


from _native_base import _NativeBase

import generated


class ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform):
            super().__init__(args[0])
        else:
            super().__init__(generated.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def some_lambda(self) -> ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda:
        """"""
        return _wrap(self._native.some_lambda, ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda)
    @some_lambda.setter
    def some_lambda(self, value: ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda):
      self._native.some_lambda = _unwrap(value, ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda)


    def use_lambda(self, some_lambda: ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda) -> ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda:
        """"""
        return _wrap(self._native.use_lambda(_unwrap(some_lambda, ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda)), ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda)

