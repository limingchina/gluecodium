

from smoke.ParentClass import ParentClass
from enum import Enum
import typing

class ForwardDeclarationBug(
    ParentClass):

    def foo(self, bar: ParentClass):
        ...


