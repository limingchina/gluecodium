

from smoke.ParentClass import ParentClass
import typing

class ForwardDeclarationBug(
    ParentClass):

    def foo(self, bar: ParentClass):
        ...

