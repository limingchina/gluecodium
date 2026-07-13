

from smoke.InterfaceWithLambda import InterfaceWithLambda

from _native_base import _NativeBase


class ChildClassWithLambda(
    InterfaceWithLambda)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

