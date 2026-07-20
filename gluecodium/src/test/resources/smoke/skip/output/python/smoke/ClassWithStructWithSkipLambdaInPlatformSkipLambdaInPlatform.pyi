

from smoke.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda import ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda
import typing


from _native_base import _NativeBase

import generated


class ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform):
            super().__init__(args[0])
        else:
            super().__init__(generated.ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def some_lambda(self) -> ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda:
        """"""
        return ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda(self._native.some_lambda)
    @some_lambda.setter
    def some_lambda(self, value: ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda):
      self._native.some_lambda = getattr(value, "_native", value)


    def use_lambda(self, some_lambda: ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda) -> ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatformSomeLambda: ...

