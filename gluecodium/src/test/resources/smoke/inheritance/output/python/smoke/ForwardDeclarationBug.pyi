

from smoke.ParentClass import ParentClass
from enum import Enum
import typing
from typing import Optional

class ForwardDeclarationBug(
    ParentClass):

    def foo(self, bar: ParentClass):
        ...
