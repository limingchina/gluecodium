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

"""@Internal visibility tests for the Python (pybind11) bindings.

The @Internal attribute marks elements as library-internal API. Python has no
formal access-control keyword, so internal elements are emitted with a single
leading underscore (_), following PEP 8's convention for non-public API.
This keeps them reachable (as internal features may be relied upon by other
generated code or same-package callers) while clearly signaling non-public intent.
"""

import pytest


# ---------------------------------------------------------------------------
# Internal types are importable under underscore-prefixed names
# ---------------------------------------------------------------------------

def test_internal_types_are_exposed_with_underscore_prefix():
    """@Internal types should be importable under their underscore-prefixed names."""
    from test._InternalAttributeClassWithFunctions import _InternalAttributeClassWithFunctions
    from test._InternalAttributeClassWithStaticProperty import _InternalAttributeClassWithStaticProperty
    from test._InternalAttributeInterfaceParent import _InternalAttributeInterfaceParent
    from test._SomeInternalStructWithMembers import _SomeInternalStructWithMembers
    from test._SomeInternalClassWithMembers import _SomeInternalClassWithMembers
    from test._SomeOpenInternalClass import _SomeOpenInternalClass
    from test._SomeDerivedInternalClass import _SomeDerivedInternalClass
    from test._SomeInternalEnum import _SomeInternalEnum
    from test._SomethingBadHappenedError import _SomethingBadHappenedError

    # Internal enum members should be accessible
    assert _SomeInternalEnum.ONE is not None
    assert _SomeInternalEnum.TWO is not None
    assert _SomeInternalEnum.THREE is not None

    # Internal enum member that is itself @Internal should have underscore prefix
    assert hasattr(_SomeInternalEnum, "_SINGLE")
    assert _SomeInternalEnum._SINGLE is not None


def test_internal_types_not_exposed_without_underscore():
    """@Internal types should NOT be importable under their original (non-prefixed) names."""
    with pytest.raises(ImportError):
        from test.InternalAttributeClassWithFunctions import InternalAttributeClassWithFunctions
    with pytest.raises(ImportError):
        from test.SomeInternalEnum import SomeInternalEnum


# ---------------------------------------------------------------------------
# Internal fields on public structs
# ---------------------------------------------------------------------------

def test_public_struct_with_internal_fields():
    """Public structs with @Internal fields: internal fields are accessible
    under underscore-prefixed names but excluded from constructor signatures."""
    from test.SomeStructWithInternalMembers import SomeStructWithInternalMembers
    from test.PublicStructWithNonDefaultInternalAttributeField import (
        PublicStructWithNonDefaultInternalAttributeField,
    )

    # The @Internal field someInternalString is excluded from the constructor
    # signature, so the constructor only takes the public fields.
    public_struct = SomeStructWithInternalMembers(123, 456)
    assert public_struct.some_integer == 123
    assert public_struct.some_long == 456

    # The internal field should be accessible under its underscore-prefixed name
    assert hasattr(public_struct, "_some_internal_string")

    # Test struct with non-default internal field
    struct_val = PublicStructWithNonDefaultInternalAttributeField(42, True)
    assert struct_val.defaulted_field == 42
    assert struct_val.public_field is True
    # The internal field should be accessible under its underscore-prefixed name
    assert hasattr(struct_val, "_internal_field")


def test_internal_fields_affect_constructor_arity():
    """@Internal fields should not appear in constructor signatures."""
    from test.SomeStructWithInternalFreeArgsCtor import SomeStructWithInternalFreeArgsCtor
    from test.SomeStructWithInternalAllArgsCtor import SomeStructWithInternalAllArgsCtor

    # Free-args ctor: internal field someInt is excluded from the constructor.
    # Only public field someString (with default "Special string") remains.
    ctor = SomeStructWithInternalFreeArgsCtor()
    assert ctor.some_string == "Special string"
    # Internal field is accessible under underscore prefix
    assert hasattr(ctor, "_some_int")

    # All-args ctor: both someInt and someString are @Internal, so the
    # constructor takes no arguments.
    ctor = SomeStructWithInternalAllArgsCtor()
    assert hasattr(ctor, "_some_int")
    assert hasattr(ctor, "_some_string")


# ---------------------------------------------------------------------------
# Internal methods on public structs/classes
# ---------------------------------------------------------------------------

def test_internal_methods_on_public_struct():
    """@Internal methods on public structs should be callable under
    underscore-prefixed names."""
    from test.SomeStructWithInternalMembers import SomeStructWithInternalMembers

    public_struct = SomeStructWithInternalMembers(1, 2)

    # Internal instance method
    assert hasattr(public_struct, "_some_internal_function")
    assert public_struct._some_internal_function() == 888

    # Internal static method
    assert hasattr(SomeStructWithInternalMembers, "_some_static_internal_function")
    assert SomeStructWithInternalMembers._some_static_internal_function() == 777

    # Internal named constructor
    assert hasattr(SomeStructWithInternalMembers, "_some_internal_ctor")
    result = SomeStructWithInternalMembers._some_internal_ctor(42)
    assert result.some_integer == 42


def test_internal_methods_on_public_class():
    """@Internal methods on public classes should be callable under
    underscore-prefixed names."""
    from test.SomeClassWithInternalMembers import SomeClassWithInternalMembers

    obj = SomeClassWithInternalMembers.create()

    # Internal instance method
    assert hasattr(obj, "_some_internal_function")
    assert obj._some_internal_function() == 567

    # Internal static method
    assert hasattr(SomeClassWithInternalMembers, "_some_static_internal_function")
    assert SomeClassWithInternalMembers._some_static_internal_function() == 123

    # Internal property
    assert hasattr(obj, "_some_internal_property")
    assert obj._some_internal_property == "DEFAULT"
    obj._some_internal_property = "modified"
    assert obj._some_internal_property == "modified"

    # Internal constant (constants are uppercased by naming rules)
    assert hasattr(SomeClassWithInternalMembers, "_INTERNAL_CONSTANT")
    assert SomeClassWithInternalMembers._INTERNAL_CONSTANT == 11


# ---------------------------------------------------------------------------
# Platform-specific @Internal
# ---------------------------------------------------------------------------

def test_platform_specific_internal():
    """Platform-specific @Internal should work correctly for Python.

    The function someInternalFunctionButOnlyForAndroid is @Internal(Java, Kotlin)
    but NOT @Internal(Python), so it should be public in Python (no underscore).
    """
    from test.SomeStructWithInternalMembers import SomeStructWithInternalMembers

    public_struct = SomeStructWithInternalMembers(1, 2)
    # This function is @Internal(Java, Kotlin) so should be public in Python
    assert hasattr(public_struct, "some_internal_function_but_only_for_android")
    assert not hasattr(public_struct, "_some_internal_function_but_only_for_android")
    result = public_struct.some_internal_function_but_only_for_android()
    assert result == 999


def test_platform_reverse_internal_not_prefixed():
    """Types with @Internal(Java), @Internal(Kotlin), etc. (platform-scoped)
    should NOT be internal for Python — no underscore prefix."""
    from test.JavaInternalClassRev import JavaInternalClassRev
    from test.KotlinInternalClassRev import KotlinInternalClassRev
    from test.SwiftInternalClassRev import SwiftInternalClassRev
    from test.DartInternalClassRev import DartInternalClassRev
    from test.JavaSwiftInternalClass import JavaSwiftInternalClass

    # All these types have platform-scoped @Internal, not global @Internal,
    # so they should be public for Python (no underscore prefix).
    # If they were importable without underscore, the test passes.
    assert JavaInternalClassRev is not None
    assert KotlinInternalClassRev is not None
    assert SwiftInternalClassRev is not None
    assert DartInternalClassRev is not None
    assert JavaSwiftInternalClass is not None


# ---------------------------------------------------------------------------
# Internal nested types
# ---------------------------------------------------------------------------

def test_internal_nested_types():
    """Internal nested types should be accessible under underscore-prefixed names."""
    from test._SomeInternalClassWithMembers import _SomeInternalClassWithMembers

    # Nested internal class should have underscore prefix
    assert hasattr(_SomeInternalClassWithMembers, "_SomeNestedInternalClass")

    # Create an instance of the nested internal class
    nested = _SomeInternalClassWithMembers._SomeNestedInternalClass.create()
    assert nested.do_something() == 1
    # The @Internal method do_something_else should have underscore prefix
    assert hasattr(nested, "_do_something_else")
    assert nested._do_something_else() == 2


# ---------------------------------------------------------------------------
# Internal struct with members
# ---------------------------------------------------------------------------

def test_internal_struct_with_members():
    """Internal struct should be fully functional under underscore-prefixed name."""
    from test._SomeInternalStructWithMembers import _SomeInternalStructWithMembers

    obj = _SomeInternalStructWithMembers.create()
    assert obj.some_integer == 123
    assert obj.some_long == 456
    assert obj.some_function() == 32


# ---------------------------------------------------------------------------
# Internal class with static property
# ---------------------------------------------------------------------------

def test_internal_class_with_static_property():
    """Internal class with @Internal static property should have both
    the class and property under underscore-prefixed names."""
    from test._InternalAttributeClassWithStaticProperty import (
        _InternalAttributeClassWithStaticProperty,
    )

    # The @Internal property foo_bar should have underscore prefix.
    # Static properties are exposed as static methods (pybind11 limitation),
    # so they must be called rather than accessed as attributes.
    assert hasattr(_InternalAttributeClassWithStaticProperty, "_foo_bar")
    assert _InternalAttributeClassWithStaticProperty._foo_bar() == "foo"


# ---------------------------------------------------------------------------
# Internal class with members
# ---------------------------------------------------------------------------

def test_internal_class_with_members():
    """Internal class should be fully functional under underscore-prefixed name."""
    from test._SomeInternalClassWithMembers import _SomeInternalClassWithMembers

    obj = _SomeInternalClassWithMembers.create()
    assert obj.some_function() == 987
    assert _SomeInternalClassWithMembers.some_static_function() == 765


# ---------------------------------------------------------------------------
# Internal derived class
# ---------------------------------------------------------------------------

def test_internal_derived_class():
    """Internal derived class should be functional under underscore-prefixed name."""
    from test._SomeDerivedInternalClass import _SomeDerivedInternalClass

    obj = _SomeDerivedInternalClass._create()
    assert obj._some_function_from_derived_class() == 111
    # Inherited from SomeInternalInterface
    assert obj.foo() == 222
    assert obj.bar() == 333
    # Inherited from SomeOpenInternalClass
    assert obj._some_internal_function() == 444


# ---------------------------------------------------------------------------
# InternalFields.lime tests
# ---------------------------------------------------------------------------

def test_internal_fields_with_defaults():
    """Structs from InternalFields.lime: internal fields with defaults
    should be accessible under underscore-prefixed names but excluded
    from constructor signatures."""
    from test.PublicFieldsNone import PublicFieldsNone
    from test.PublicFieldsNoInit import PublicFieldsNoInit
    from test.PublicFieldsAllInit import PublicFieldsAllInit
    from test.PublicFieldsMixedInit import PublicFieldsMixedInit

    # PublicFieldsNone: only field is @Internal with default
    # Should be default-constructible (no public fields)
    obj = PublicFieldsNone()
    assert hasattr(obj, "_internal_field")
    assert obj._internal_field == "foo"

    # PublicFieldsNoInit: public field (no default) + internal field (with default)
    # Constructor takes only the public field
    obj = PublicFieldsNoInit("hello")
    assert obj.public_field == "hello"
    assert hasattr(obj, "_internal_field")
    assert obj._internal_field == "foo"

    # PublicFieldsAllInit: public field (with default) + internal field (with default)
    # Should be default-constructible
    obj = PublicFieldsAllInit()
    assert obj.public_field == "bar"
    assert hasattr(obj, "_internal_field")
    assert obj._internal_field == "foo"

    # PublicFieldsMixedInit: public1 (default), public2 (no default), internal (default)
    # Constructor takes only the non-default public field
    obj = PublicFieldsMixedInit("value2")
    assert obj.public_field1 == "bar"
    assert obj.public_field2 == "value2"
    assert hasattr(obj, "_internal_field")
    assert obj._internal_field == "foo"
