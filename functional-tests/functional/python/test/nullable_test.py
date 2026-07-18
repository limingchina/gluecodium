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

"""Nullability mapping tests for the Python (pybind11) bindings."""

import functional
from test.NullableCollections import NullableCollections, UseNullableCollections

import pytest


class TestNullable:
    def test_nullable_list_round_trip(self):
        input_list = ["a", "b", "c"]
        result = UseNullableCollections.nullable_list_round_trip(input_list)

        assert result == input_list

    def test_nullable_list_null_round_trip(self):
        result = UseNullableCollections.nullable_list_round_trip(None)

        assert result is None

    def test_nullable_collections_struct(self):
        struct = NullableCollections()
        struct.list_field = ["x", "y"]
        result = UseNullableCollections.nullable_collections_round_trip(struct)

        assert result.list_field == ["x", "y"]
