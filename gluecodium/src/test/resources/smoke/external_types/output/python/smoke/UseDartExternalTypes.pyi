

from smoke.CompressionState import CompressionState
from smoke.DartColor import DartColor
from smoke.DartSeason import DartSeason
from smoke.Rectangle import Rectangle

from _native_base import _NativeBase


class UseDartExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def rectangle_round_trip(self, input: Rectangle) -> Rectangle:
        """"""
        return self._native.rectangle_round_trip(input)


    def compression_state_round_trip(self, input: CompressionState) -> CompressionState:
        """"""
        return self._native.compression_state_round_trip(input)


    def color_round_trip(self, input: DartColor) -> DartColor:
        """"""
        return self._native.color_round_trip(input)


    def season_round_trip(self, input: DartSeason) -> DartSeason:
        """"""
        return self._native.season_round_trip(input)

