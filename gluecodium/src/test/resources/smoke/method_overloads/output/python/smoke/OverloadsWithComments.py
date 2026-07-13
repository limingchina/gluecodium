

from __future__ import annotations



from _native_base import _NativeBase

import generated


class OverloadsWithComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_stuff(self):
        """"""
        return self._native.do_stuff()

    [stuff]
    def do_stuff(self, stuff: str):
        """[stuff]"""
        return self._native.do_stuff(stuff)

