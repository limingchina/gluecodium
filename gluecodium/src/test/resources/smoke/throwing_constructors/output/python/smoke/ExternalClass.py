

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.ErrorEnum import ErrorEnum
from smoke.ExternalClass import ExternalClass
from smoke.InternalOne import InternalOne
from smoke.InternalTwo import InternalTwo

class ExternalClass:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> ExternalClass:
        """"""
        return self._native.create()

