

from __future__ import annotations

from smoke.CompressionState import CompressionState
from smoke.DartColor import DartColor
from smoke.DartSeason import DartSeason
from smoke.Rectangle import Rectangle


from _native_base import _NativeBase

import generated


class UseDartExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def rectangle_round_trip(input: Rectangle) -> Rectangle:
        """"""
        native_result = generated.UseDartExternalTypes.rectangle_round_trip(input._native)
        return Rectangle(native_result)

    @staticmethod
    def compression_state_round_trip(input: CompressionState) -> CompressionState:
        """"""
        native_result = generated.UseDartExternalTypes.compression_state_round_trip(input._native)
        return CompressionState(native_result)

    @staticmethod
    def color_round_trip(input: DartColor) -> DartColor:
        """"""
        native_result = generated.UseDartExternalTypes.color_round_trip(input._native)
        return DartColor(native_result)

    @staticmethod
    def season_round_trip(input: DartSeason) -> DartSeason:
        """"""
        native_result = generated.UseDartExternalTypes.season_round_trip(input._native)
        return DartSeason(native_result)

