# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Struct mapping tests for the Python (pybind11) bindings."""

import functional
from test.PlainDataStructures import PlainDataStructures
from test.PlainDataStructuresColor import PlainDataStructuresColor as Color
from test.PlainDataStructuresColoredLine import PlainDataStructuresColoredLine as ColoredLine
from test.PlainDataStructuresLine import PlainDataStructuresLine as Line
from test.PlainDataStructuresPoint import PlainDataStructuresPoint as Point

import pytest


class TestStructs:
    def test_create_point(self):
        point = PlainDataStructures.create_point(1.0, 2.0)

        assert isinstance(point, Point)
        assert point.x == 1.0
        assert point.y == 2.0

    def test_swap_point_coordinates(self):
        point = PlainDataStructures.create_point(1.0, 2.0)
        swapped = PlainDataStructures.swap_point_coordinates(point)

        assert swapped.x == 2.0
        assert swapped.y == 1.0

    def test_nested_struct(self):
        line = PlainDataStructures.create_line(Point(1.0, 2.0), Point(3.0, 4.0))

        assert isinstance(line, Line)
        assert line.a.x == 1.0
        assert line.b.y == 4.0

    def test_colored_line(self):
        line = PlainDataStructures.create_line(Point(0.0, 0.0), Point(1.0, 1.0))
        color = Color(10, 20, 30)
        colored = PlainDataStructures.create_colored_line(line, color)

        assert isinstance(colored, ColoredLine)
        assert colored.color.red == 10
        assert colored.line.b.x == 1.0

    def test_struct_field_mutation(self):
        point = Point(0.0, 0.0)
        point.x = 5.0

        assert point.x == 5.0
