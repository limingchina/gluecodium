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

"""Collection (List/Set/Map) mapping tests for the Python (pybind11) bindings."""

import functional
from test.Arrays import Arrays
from test.Maps import Maps
from test.SetType import SetType

import pytest


class TestCollections:
    def test_reverse_string_array(self):
        result = Arrays.reverse_string_array(["a", "b", "c"])

        assert result == ["c", "b", "a"]

    def test_reverse_int_array(self):
        result = Arrays.reverse_int32_array([1, 2, 3])

        assert result == [3, 2, 1]

    def test_map_method(self):
        input_map = {1: "one", 2: "two"}
        result = Maps.method_with_map(input_map)

        assert result == {1: "ONE", 2: "TWO"}

    def test_set_round_trip(self):
        input_set = {"x", "y", "z"}
        result = SetType.string_set_round_trip(input_set)

        assert result == input_set
