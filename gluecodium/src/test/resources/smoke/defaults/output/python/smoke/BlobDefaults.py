

from __future__ import annotations



from _native_base import _NativeBase

import generated


class BlobDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], BlobDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.BlobDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def empty_list(self) -> bytes:
        """"""
        return self._native.empty_list

    @empty_list.setter
    def empty_list(self, value: bytes):
      self._native.empty_list = getattr(value, "_native", value)



    @property
    def dead_beef(self) -> bytes:
        """"""
        return self._native.dead_beef

    @dead_beef.setter
    def dead_beef(self, value: bytes):
      self._native.dead_beef = getattr(value, "_native", value)


