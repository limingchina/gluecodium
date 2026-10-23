

from enum import Enum
import typing
from typing import Optional

class AsyncWithSkips:

    @typing.overload
    @staticmethod
    def make_shared_instance(android_context: str):
        ...

    @typing.overload
    @staticmethod
    def make_shared_instance():
        ...
