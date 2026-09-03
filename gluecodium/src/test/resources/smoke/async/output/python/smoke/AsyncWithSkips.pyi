

from enum import Enum
import typing

class AsyncWithSkips:

    @typing.overload
    @staticmethod
    def make_shared_instance(android_context: str):
        ...

    @typing.overload
    @staticmethod
    def make_shared_instance():
        ...


