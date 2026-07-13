

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.ErrorEnum import ErrorEnum
from smoke.ExternalClass import ExternalClass
from smoke.InternalOne import InternalOne
from smoke.InternalTwo import InternalTwo

from _native_base import _NativeBase


class ExternalClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self) -> ExternalClass:
        """"""
        return self._native.create()

