

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Comments import Comments

class CommentsLinks(_NativeBase):
    """The nested types like `CommentsLinks.random_method` don't need full name prefix, but it's
possible to references other interfaces like `CommentsInterface` or other members
`Comments.some_method_with_all_comments`.

Weblinks are not modified like this [example1], [example2](http://www.example.com/2) or https://www.example.com/3.

[example1]: http://example.com/1"""
    def __init__(self, native):
        super().__init__(native)

    def random_method(self, *args, **kwargs) -> Comments.SomeEnum:
        """Link types:
* constant: `Comments.VERY_USEFUL`
* struct: `Comments.SomeStruct`
* struct field: `Comments.SomeStruct.some_field`
* enum: `Comments.SomeEnum`
* enum item: `Comments.SomeEnum.USEFUL`
* property: `Comments.is_some_property`
* property setter: `Comments.is_some_property`
* property getter: `Comments.is_some_property`
* method: `Comments.some_method_with_all_comments`
* method with signature: `Comments.one_parameter_comment_only`
* method with signature with no spaces: `Comments.one_parameter_comment_only`
* parameter: `CommentsLinks.random_method.input_parameter`
* top level constant: `CommentsTypeCollection.TYPE_COLLECTION_CONSTANT`
* top level struct: `CommentsTypeCollection.TypeCollectionStruct`
* top level struct field: `CommentsTypeCollection.TypeCollectionStruct.field`
* top level enum: `CommentsTypeCollection.TypeCollectionEnum`
* top level enum item: `CommentsTypeCollection.TypeCollectionEnum.ITEM`
* error: `Comments.SomethingWrongError`
* lambda: `Comments.SomeLambda`
* type from aux sources, same package: `AuxClass`
* type from aux sources, different package: `AuxStruct`
  * we can also have
  * nested lists

Not working for Java:
* typedef: `Comments.Usefulness`
* top level typedef: `CommentsTypeCollection.TypeCollectionTypedef`

Not working for Swift:
* named comment: []`Comments.VERY_USEFUL`"""
        return _wrap(self._native.random_method(*[_unwrap(a) for a in args]), Comments.SomeEnum)


    class RandomStruct(_NativeBase):
        """Links also work in:"""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CommentsLinks.RandomStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_CommentsLinks.RandomStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def random_field(self) -> Comments.SomeStruct:
            """Some random field `Comments.SomeStruct`"""
            return _wrap(self._native.random_field, Comments.SomeStruct)
        @random_field.setter
        def random_field(self, value: Comments.SomeStruct):
          self._native.random_field = _unwrap(value, Comments.SomeStruct)
    
    
    

