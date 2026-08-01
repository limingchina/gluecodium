

from smoke.ListenerInterface import ListenerInterface
from enum import Enum
import typing

class Weakling:

    @property
    def listener(self):
        ...

    @listener.setter
    def listener(self, value) -> None:
        ...


