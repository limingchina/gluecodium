

from package.Interface import Interface
from package.typesenum import typesenum
from package.typesexception import typesexception
from package.typesstruct import typesstruct
import typing

class Class(
    Interface):

    @staticmethod
    def constructor() -> Class:
        ...

    def fun(self, double: list[typesstruct]) -> typesstruct:
        ...

    @property
    def property(self) -> typesenum:
        ...

    @property.setter
    def property(self, value: typesenum) -> None:
        ...

