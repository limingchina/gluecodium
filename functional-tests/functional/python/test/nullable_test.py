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
from test.NullableCollections import NullableCollections
from test.UseNullableCollections import UseNullableCollections
from test.NullableStatic import NullableStatic
from test.NullablePayload import NullablePayload
from test.NullableInstanceListener import NullableInstanceListener

import pytest


class TestNullable:
    def test_nullable_class_none(self):
        assert NullableStatic.nullable_top_down_round_trip(None) is None

    def test_nullable_class_cached(self):
        value = NullablePayload.create()
        assert NullableStatic.nullable_top_down_round_trip(value) is value

    def test_nullable_class_cache_miss(self):
        value = NullablePayload(functional.test_NullablePayload.create())
        result = NullableStatic.nullable_top_down_round_trip(value)
        assert isinstance(result, NullablePayload)
        assert result.poke()

    @pytest.mark.parametrize("value", [None, NullableStatic.NullableStruct()])
    def test_nullable_struct_return(self, value):
        result = NullableStatic.nullable_struct_round_trip(value)
        if value is None:
            assert result is None
        else:
            assert isinstance(result, NullableStatic.NullableStruct)
            assert result.nullable_field is None

    @pytest.mark.parametrize("name", [None, "FIRST", "SECOND"])
    def test_nullable_enum_return(self, name):
        value = None if name is None else getattr(NullableStatic.NullableEnum, name)
        assert NullableStatic.nullable_enum_round_trip(value) is value

    def test_nullable_interface_return(self):
        value = NullableInstanceListener()
        assert NullableStatic.nullable_interface_round_trip(value) is value
        assert NullableStatic.nullable_interface_round_trip(None) is None

    def test_nullable_collection_of_wrappers(self):
        value = NullablePayload.create()
        result = NullableStatic.nullable_payload_list_round_trip([value, None])
        assert result[0] is value
        assert result[1] is None
        assert NullableStatic.nullable_payload_list_round_trip(None) is None

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
