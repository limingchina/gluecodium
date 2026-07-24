

import typing


from _native_base import _NativeBase

import generated


class BlobDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.BlobDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.BlobDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def empty_list(self) -> bytes:
        """"""
        return _wrap(self._native.empty_list, bytes)
    @empty_list.setter
    def empty_list(self, value: bytes):
      self._native.empty_list = _unwrap(value, bytes)



    @property
    def dead_beef(self) -> bytes:
        """"""
        return _wrap(self._native.dead_beef, bytes)
    @dead_beef.setter
    def dead_beef(self, value: bytes):
      self._native.dead_beef = _unwrap(value, bytes)


