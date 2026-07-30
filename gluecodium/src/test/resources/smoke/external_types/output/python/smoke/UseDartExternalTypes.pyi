

from smoke.CompressionState import CompressionState
from smoke.DartColor import DartColor
from smoke.DartSeason import DartSeason
from smoke.Rectangle import Rectangle
import typing

class UseDartExternalTypes:

    @staticmethod
    def rectangle_round_trip(input: Rectangle) -> Rectangle:
        ...

    @staticmethod
    def compression_state_round_trip(input: CompressionState) -> CompressionState:
        ...

    @staticmethod
    def color_round_trip(input: DartColor) -> DartColor:
        ...

    @staticmethod
    def season_round_trip(input: DartSeason) -> DartSeason:
        ...

