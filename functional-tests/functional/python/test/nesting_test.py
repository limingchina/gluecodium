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

"""Nesting mapping tests for the Python (pybind11) bindings."""

from test.OuterStruct import OuterStruct


class TestNesting:
    def test_nested_struct(self):
        outer = OuterStruct("hello")
        inner = OuterStruct.InnerStruct()

        assert isinstance(outer, OuterStruct)
        assert outer.field == "hello"
        assert isinstance(inner, OuterStruct.InnerStruct)
        assert inner.other_field == []

    def test_nested_struct_mutation(self):
        inner = OuterStruct.InnerStruct()
        inner.other_field = []

        assert inner.other_field == []
