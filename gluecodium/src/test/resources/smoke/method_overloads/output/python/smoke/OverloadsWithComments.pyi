

from enum import Enum
import typing

class OverloadsWithComments:

    def do_stuff(self):
        ...

    def do_stuff(self, stuff: str):
        """`OverloadsWithComments.do_stuff.stuff`"""
        ...


