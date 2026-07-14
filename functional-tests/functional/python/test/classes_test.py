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

"""Class instantiation and method tests for the Python (pybind11) bindings."""

import functional
from test.NestedInstantiableOne import NestedInstantiableOne
from test.SimpleInstantiableOne import SimpleInstantiableOne

import pytest


class TestClasses:
    def test_set_same_type_instances(self):
        input1 = SimpleInstantiableOne.create("one")
        input2 = SimpleInstantiableOne.create("two")
        nested = NestedInstantiableOne.create()

        nested.set_same_type_instances(input1, input2)
        result1 = nested.get_instance_one()
        result2 = nested.get_instance_two()

        assert result1.get_string_value() == "one"
        assert result2.get_string_value() == "two"

    def test_set_and_get_string_value(self):
        instance = SimpleInstantiableOne.create("value")

        instance.set_string_value("updated")

        assert instance.get_string_value() == "updated"
