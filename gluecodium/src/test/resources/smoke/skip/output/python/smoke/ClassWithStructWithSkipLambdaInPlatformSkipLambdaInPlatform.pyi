

from smoke.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda import ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda
import typing
from typing import Callable


from _native_base import _NativeBase

import generated


class ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def some_lambda(self) -> Callable[[], int]:
        """"""
        return _wrap(self._native.some_lambda, Callable[[], int])
    @some_lambda.setter
    def some_lambda(self, value: Callable[[], int]):
      self._native.some_lambda = _unwrap(value, Callable[[], int])


    def use_lambda(self, some_lambda: Callable[[], int]) -> Callable[[], int]: ...

