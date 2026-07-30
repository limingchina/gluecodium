

from smoke.ListenerInterface import ListenerInterface
import typing

class Weakling:

    @property
    def listener(self):
        ...

    @listener.setter
    def listener(self, value) -> None:
        ...

