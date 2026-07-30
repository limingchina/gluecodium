

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor
import typing

class ChildWithCustomConstructor(
    ParentWithCustomConstructor):

    @staticmethod
    def make() -> ChildWithCustomConstructor:
        ...

