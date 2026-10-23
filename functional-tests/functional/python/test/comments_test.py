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

"""Comment preservation tests for the Python bindings."""

import functional
import pytest


def test_comments_class_docstring():
    """Test that class-level comments are preserved as Python docstrings."""
    from test.Comments import Comments
    assert Comments.__doc__ == "This is some very useful ."
    
def test_comments_function_docstring():
    """Test that function-level comments are preserved as Python docstrings."""
    from test.Comments import Comments
    assert Comments.some_method_with_all_comments.__doc__ == "This is some very useful method that measures the usefulness of its input."
    assert Comments.some_method_with_input_comments.__doc__ == "This is some very useful method that measures the usefulness of its input."
    assert Comments.some_method_with_output_comments.__doc__ == "This is some very useful method that measures the usefulness of its input."
    
def test_comments_no_function_docstring():
    """Test that functions without comments don't emit empty docstrings."""
    from test.Comments import Comments
    assert Comments.some_method_with_nothing.__doc__ is None
    
def test_comments_property_docstring():
    """Test that property comments are preserved as Python docstrings."""
    from test.Comments import Comments
    assert Comments.is_some_attribute.__doc__ == "Some very useful attribute."

def test_comments_constant_comment():
    """Test that module-level constant comments are preserved as Python comments."""
    import inspect
    from test.Comments import Comments
    source = inspect.getsource(Comments)
    assert "#: This is some very useful constant." in source
    assert "VERY_USEFUL = True" in source

def test_comments_interface_docstring():
    """Test that interface comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.__doc__ == "This is some very useful interface."

def test_comments_interface_function_docstrings():
    """Test that interface method comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.some_method_with_all_comments.__doc__ == "This is some very useful method that measures the usefulness of its input."

def test_comments_interface_property_docstrings():
    """Test that interface property comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.is_some_attribute.__doc__ == "Some very useful attribute."

def test_comments_interface_constant_comment():
    """Test that interface constant comments are preserved as Python comments."""
    import inspect
    from another.CommentsInterface import CommentsInterface
    source = inspect.getsource(CommentsInterface)
    assert "#: This is some very useful constant." in source
    assert "VERY_USEFUL = True" in source

def test_comments_struct_docstring():
    """Test that struct comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.SomeStruct.__doc__ == "This is some very useful struct."

def test_comments_interface_nested_struct_field_comment():
    """Test that struct field comments are preserved as Python docstrings."""
    import inspect
    from another.CommentsInterface import CommentsInterface
    source = inspect.getsource(CommentsInterface.SomeStruct)
    assert '"""How useful this struct is"""' in source

def test_comments_interface_enum_docstring():
    """Test that enum comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.SomeCommentedEnum.__doc__ == "This is some very useful enum."

def test_comments_stub_class_docstring():
    """Test that stub class comments are preserved as Python docstrings."""
    from test.Comments import Comments
    assert Comments.__doc__ == "This is some very useful ."

def test_comments_stub_function_docstrings():
    """Test that stub function docstrings are preserved."""
    from test.Comments import Comments
    assert Comments.some_method_with_all_comments.__doc__ == "This is some very useful method that measures the usefulness of its input."
    
def test_comments_stub_no_function_docstring():
    """Test that stub functions without comments don't emit empty docstrings."""
    from test.Comments import Comments
    assert Comments.some_method_with_nothing.__doc__ is None

def test_comments_stub_property_docstrings():
    """Test that stub property docstrings are preserved."""
    from test.Comments import Comments
    assert Comments.is_some_attribute.__doc__ == "Some very useful attribute."

def test_comments_stub_constant_comment():
    """Test that stub constant comments are preserved as Python comments."""
    import inspect
    from test.Comments import Comments
    source = inspect.getsource(Comments)
    assert "#: This is some very useful constant." in source
    assert "VERY_USEFUL = True" in source

def test_comments_stub_interface_docstring():
    """Test that stub interface comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.__doc__ == "This is some very useful interface."

def test_comments_stub_nested_struct_docstring():
    """Test that stub struct comments are preserved as Python docstrings."""
    from another.CommentsInterface import CommentsInterface
    assert CommentsInterface.SomeStruct.__doc__ == "This is some very useful struct."

def test_comments_stub_nested_struct_field_comment():
    """Test that stub struct field comments are preserved as Python docstrings."""
    import inspect
    from another.CommentsInterface import CommentsInterface
    source = inspect.getsource(CommentsInterface.SomeStruct)
    assert '"""How useful this struct is"""' in source


def test_doc_reference_class_level():
    """Test that class-level doc comment references to other types and members are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.__doc__
    # Relative reference to a method within the same class
    assert "`CommentsLinks.random_method`" in doc
    # Cross-package reference to an interface
    assert "`CommentsInterface`" in doc
    # Reference to a method in another class (snake_case conversion)
    assert "`Comments.some_method_with_all_comments`" in doc
    # Raw bracket references should NOT remain for resolved links
    assert "[random_method]" not in doc
    assert "[another.CommentsInterface]" not in doc
    assert "[comments.someMethodWithAllComments]" not in doc

def test_doc_reference_constant():
    """Test that doc references to constants are resolved with UPPER_SNAKE_CASE."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`Comments.VERY_USEFUL`" in doc
    assert "[comments.VeryUseful]" not in doc

def test_doc_reference_struct_and_field():
    """Test that doc references to structs and struct fields are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`Comments.SomeStruct`" in doc
    assert "`Comments.SomeStruct.some_field`" in doc
    assert "[comments.SomeStruct]" not in doc
    assert "[comments.SomeStruct.someField]" not in doc

def test_doc_reference_enum_and_enumerator():
    """Test that doc references to enums and enum items are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`Comments.SomeCommentedEnum`" in doc
    assert "`Comments.SomeCommentedEnum.USEFUL`" in doc
    assert "[comments.SomeCommentedEnum]" not in doc
    assert "[comments.SomeCommentedEnum.Useful]" not in doc

def test_doc_reference_property():
    """Test that doc references to properties are resolved with Python naming."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    # Boolean property gets 'is_' prefix in Python
    assert "`Comments.is_some_attribute`" in doc
    assert "[comments.SomeAttribute]" not in doc

def test_doc_reference_method():
    """Test that doc references to methods are resolved with snake_case."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`Comments.instance_method`" in doc
    assert "[comments.instanceMethod]" not in doc

def test_doc_reference_top_level_elements():
    """Test that doc references to top-level constants, structs, enums, and fields are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`CommentsTypeCollection.TYPE_COLLECTION_CONSTANT`" in doc
    assert "`CommentsTypeCollection.TypeCollectionStruct`" in doc
    assert "`CommentsTypeCollection.TypeCollectionStruct.field`" in doc
    assert "`CommentsTypeCollection.TypeCollectionEnum`" in doc
    assert "`CommentsTypeCollection.TypeCollectionEnum.ITEM`" in doc

def test_doc_reference_error():
    """Test that doc references to exceptions are resolved with Error suffix."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    # The LIME exception 'TooUseful' becomes 'TooUsefulError' in Python
    assert "`CommentsLinks.TooUsefulError`" in doc
    assert "[TooUseful]" not in doc

def test_doc_reference_typealias():
    """Test that doc references to type aliases are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    assert "`Comments.Usefulness`" in doc
    assert "`Comments.SomeArray`" in doc
    assert "`Comments.SomeMap`" in doc
    assert "`CommentsTypeCollection.TypeCollectionTypedef`" in doc

def test_doc_reference_parameter():
    """Test that doc references to function parameters are resolved."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    # Parameter reference resolves to the fully-qualified path
    assert "`CommentsLinks.random_method.input_parameter`" in doc
    assert "[inputParameter]" not in doc

def test_doc_reference_unresolved_remains():
    """Test that references to non-existent elements remain as raw brackets."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    # 'outputParameter' doesn't exist, so it should remain unresolved
    assert "[outputParameter]" in doc

def test_comments_escaped_brackets():
    """Test that escaped square brackets in comments are rendered as literal brackets without backslashes."""
    from test.CommentsLinks import CommentsLinks
    doc = CommentsLinks.random_method.__doc__
    # Escaped brackets \[0, 23\] should appear as literal [0, 23] in the docstring
    assert "[0, 23]" in doc
    assert "\\[0, 23\\]" not in doc