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

"""Listeners with return values tests for the Python (pybind11) bindings.

Tests that a Python subclass of ListenerWithReturn can override the
interface methods and that C++ can call them through the trampoline
and receive the correct return values for various types (String, struct,
enum, list, map, Blob, class instances).

Key pattern: the trampoline uses PYBIND11_OVERRIDE_PURE with the C++ method
name (e.g. ``get_message``).  A Python subclass overrides that *method* (not
the Python property, if any) so the trampoline can discover and dispatch to
it.  Return values must be native pybind11 objects (not Python wrapper
objects) because the trampoline's type caster only recognises the pybind11
types.
"""

import functional
from test.ListenerWithReturn import ListenerWithReturn
from test.MessageDelivery import MessageDelivery
from test.MessagePackage import MessagePackage
from test.MessageBox import MessageBox

import pytest


class _TestMessagePackage(MessagePackage):
    """Python implementation of MessagePackage that returns 'Works'."""
    def __init__(self):
        super().__init__()

    def unpack_message(self) -> str:
        return "Works"


class _TestListener(ListenerWithReturn):
    """Python implementation of ListenerWithReturn returning 'Works' for all methods."""

    def __init__(self):
        super().__init__()

    def get_message(self) -> str:
        return "Works"

    def get_packed_message(self):
        return _TestMessagePackage()

    def get_boxed_message(self):
        # MessageBox extends _NativeBase (not the pybind11 class), so return
        # the native pybind11 object directly for the trampoline type caster.
        return functional.test_MessageBox.create()

    def get_structured_message(self):
        # Return the native pybind11 struct, not the Python wrapper, because the
        # trampoline's type caster only recognises pybind11 struct instances.
        return functional.test_ListenerWithReturn.MessageStruct("Works")

    def get_enumerated_message(self):
        # Return the native pybind11 enum value, not the Python wrapper enum.
        return functional.test_ListenerWithReturn.MessageEnum.YES

    def get_arrayed_message(self) -> list:
        return ["Works"]

    def get_mapped_message(self) -> dict:
        return {0: "Works"}

    def get_buffered_message(self) -> bytes:
        return b"Works"


class TestListenersReturnValues:
    def setup_method(self):
        self._envelope = _TestListener()
        self._delivery = MessageDelivery.create_me()

    def test_string_return(self):
        assert self._delivery.get_message(self._envelope) == "Works"

    def test_package_return(self):
        assert self._delivery.get_packed_message(self._envelope) == "Works"

    def test_boxed_return(self):
        assert self._delivery.get_boxed_message(self._envelope) == "Works"

    def test_struct_return(self):
        assert self._delivery.get_structured_message(self._envelope) == "Works"

    def test_enum_return(self):
        assert self._delivery.get_enumerated_message(self._envelope) == "YES"

    def test_array_return(self):
        assert self._delivery.get_arrayed_message(self._envelope) == "Works"

    def test_map_return(self):
        assert self._delivery.get_mapped_message(self._envelope) == "Works"

    def test_buffered_return(self):
        assert self._delivery.get_buffered_message(self._envelope) == "Works"
