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

"""@Internal visibility filtering tests for the Python (pybind11) bindings.

The @Internal attribute suppresses Python bindings for public API. This test
verifies that @Internal elements are not exposed in Python.
"""

import pytest


def test_internal_types_are_not_exposed():
    """@Internal types must not be importable or present in the Python API."""
    with pytest.raises(ImportError):
        from test.InternalAttributeClassWithFunctions import InternalAttributeClassWithFunctions

    with pytest.raises(ImportError):
        from test.InternalAttributeClassWithStaticProperty import InternalAttributeClassWithStaticProperty

    with pytest.raises(ImportError):
        from test.InternalAttributeInterfaceParent import InternalAttributeInterfaceParent

    with pytest.raises(ImportError):
        from test.SomeInternalLambda import SomeInternalLambda

    with pytest.raises(ImportError):
        from test.SomeInternalInterface import SomeInternalInterface

    with pytest.raises(ImportError):
        from test.SomeInternalStructWithMembers import SomeInternalStructWithMembers

    with pytest.raises(ImportError):
        from test.SomeInternalClassWithMembers import SomeInternalClassWithMembers

    with pytest.raises(ImportError):
        from test.SomeOpenInternalClass import SomeOpenInternalClass

    with pytest.raises(ImportError):
        from test.SomeDerivedInternalClass import SomeDerivedInternalClass

    with pytest.raises(ImportError):
        from test.SomeInternalEnum import SomeInternalEnum

    with pytest.raises(ImportError):
        from test.SomethingBadHappened import SomethingBadHappened


def test_internal_nested_types_are_not_exposed():
    """Types nested inside @Internal containers must not be exposed."""
    with pytest.raises(ImportError):
        from test.SomeInternalClassWithMembersSomeNestedInternalClass import SomeNestedInternalClass


def test_types_nested_in_internal_containers_are_not_exposed():
    """Types nested inside @Internal containers must not be exposed."""
    with pytest.raises(ImportError):
        from test.OuterClassWithInternalAttributeClassNestedInInternalClass import (
            ClassNestedInInternalClass,
        )

    with pytest.raises(ImportError):
        from test.OuterClassWithInternalAttributeLambdaNestedInInternalClass import (
            LambdaNestedInInternalClass,
        )

    with pytest.raises(ImportError):
        from test.OuterClassWithInternalAttributeStructNestedInInternalClass import (
            StructNestedInInternalClass,
        )


def test_public_structs_with_internal_fields():
    """Public structs with @Internal fields should be accessible, but internal fields
    and internal members should not be exposed in the Python API."""
    from test.SomeStructWithInternalMembers import SomeStructWithInternalMembers
    from test.PublicStructWithNonDefaultInternalField import PublicStructWithNonDefaultInternalField

    # The @Internal field someInternalString is filtered out, so the constructor
    # only takes the non-internal fields: someInteger and someLong.
    public_struct = SomeStructWithInternalMembers(123, 456)
    assert public_struct.some_integer == 123
    assert public_struct.some_long == 456

    # The internal field should not be accessible
    assert not hasattr(public_struct, "some_internal_string")
    # Internal methods should not be accessible
    assert not hasattr(public_struct, "some_internal_function")
    assert not hasattr(public_struct, "some_static_internal_function")

    # Test struct with non-default internal field: defaultedField (has default)
    # and publicField are public; internalField is @Internal.
    # The constructor takes only the public non-default fields.
    struct_val = PublicStructWithNonDefaultInternalField(42, True)
    assert struct_val.defaulted_field == 42
    assert struct_val.public_field is True
    # The internal field should not be accessible
    assert not hasattr(struct_val, "internal_field")


def test_platform_specific_internal():
    """Platform-specific @Internal should work correctly for Python.

    The function someInternalFunctionButOnlyForAndroid is @Internal(Java, Kotlin)
    but NOT @Internal(Python), so it should be public in Python.
    """
    from test.SomeStructWithInternalMembers import SomeStructWithInternalMembers

    public_struct = SomeStructWithInternalMembers(1, 2)
    # This function is @Internal(Java, Kotlin) so should be public in Python
    assert hasattr(public_struct, "some_internal_function_but_only_for_android")
    result = public_struct.some_internal_function_but_only_for_android()
    assert result == 999


def test_internal_fields_affect_constructor_arity():
    """@Internal fields should not affect constructor signatures in Python."""
    from test.SomeStructWithInternalFreeArgsCtor import SomeStructWithInternalFreeArgsCtor
    from test.SomeStructWithInternalAllArgsCtor import SomeStructWithInternalAllArgsCtor

    # Free-args ctor: internal field someInt is filtered out.
    # Only public field someString (with default "Special string") remains.
    # The struct should be default-constructible (someString has a default).
    ctor = SomeStructWithInternalFreeArgsCtor()
    assert ctor.some_string == "Special string"

    # All-args ctor: both someInt and someString are @Internal, so the
    # constructor takes no arguments.
    ctor = SomeStructWithInternalAllArgsCtor()
