

import typing

from _native_base import _NativeBase

import generated


class EnableIfEnabled(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def enable_if_unquoted(): ...

    @staticmethod
    def enable_if_unquoted_list(): ...

    @staticmethod
    def enable_if_quoted(): ...

    @staticmethod
    def enable_if_quoted_list(): ...

    @staticmethod
    def enable_if_tagged(): ...

    @staticmethod
    def enable_if_tagged_list(): ...

    @staticmethod
    def enable_if_mixed_list(): ...

