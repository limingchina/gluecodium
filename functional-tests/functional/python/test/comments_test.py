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