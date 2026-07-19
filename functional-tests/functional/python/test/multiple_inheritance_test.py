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

"""Multiple-inheritance tests for the Python (pybind11) bindings.

Covers the case where a derived type has more than one base class (a regular
base plus a narrow interface). The pybind11 ``py::class_`` for the derived type
must list every base class as a template argument so that (multiple) inheritance
is visible and ``std::shared_ptr`` up/down-casting between the derived type and
its bases works.
"""

import functional
from test.MultipleInheritanceFactory import MultipleInheritanceFactory
from test.MultipleInheritanceChecker import MultipleInheritanceChecker

import pytest


class TestMultipleInheritance:
    def test_multi_class_inherits_open_class(self):
        instance = MultipleInheritanceFactory.get_multi_class()
        # Inherited from OpenClass (a regular open base class): the method must be callable and
        # the property accessible through the multiple-inheritance py::class_ binding. The C++
        # fixture's setters are no-ops and getters return empty, so we only assert reachability
        # (mirroring the Swift test, which never reads a set value back).
        instance.parent_function()
        instance.parent_property
        # Own members.
        instance.child_function()
        instance.child_property

    def test_multi_class_inherits_narrow_interface(self):
        instance = MultipleInheritanceFactory.get_multi_class()
        # Inherited from NarrowInterface (a narrow base interface).
        assert instance.parent_function_light() == "foo class"
        instance.parent_property_light

    def test_multi_interface_inherits_regular_interface(self):
        instance = MultipleInheritanceFactory.get_multi_interface()
        instance.parent_function()
        instance.parent_property
        instance.child_function()
        instance.child_property

    def test_multi_interface_inherits_narrow_interface(self):
        instance = MultipleInheritanceFactory.get_multi_interface()
        assert instance.parent_function_light() == "foo interface"
        instance.parent_property_light

    def test_upcast_to_narrow(self):
        # A MultiInterface instance (which also inherits NarrowInterface) must satisfy
        # check_is_narrow: the C++ side dynamic_pointer_casts to NarrowInterface and succeeds.
        instance = MultipleInheritanceFactory.get_multi_interface()
        assert MultipleInheritanceChecker.check_is_narrow(instance)

    def test_upcast_multi_interface_to_narrow(self):
        # A NarrowInterface view of a MultiInterface must NOT satisfy check_is_multi_interface:
        # the C++ side dynamic_pointer_casts back to MultiInterface and fails (downcast is
        # impossible through the narrow interface alone). Mirrors Swift's
        # testFromSwiftSendDowncastFails.
        instance = MultipleInheritanceFactory.get_multi_interface()
        narrow = MultipleInheritanceFactory.upcast_multi_interface_to_narrow(instance)
        assert not MultipleInheritanceChecker.check_is_multi_interface(narrow)

    def test_narrow_round_trip_preserves_identity(self):
        # A narrow-interface round trip must NOT preserve identity with the C++ singleton:
        # the narrow interface intentionally breaks referential equality on the C++ -> Platform
        # -> C++ round trip (see docs/lime_idl.md). Mirrors Swift's
        # testFromCppRoundTripNotEquals.
        narrow = MultipleInheritanceFactory.get_multi_class_singleton()
        returned = MultipleInheritanceChecker.narrow_round_trip(narrow)
        assert not MultipleInheritanceChecker.check_singleton_equality(returned)
