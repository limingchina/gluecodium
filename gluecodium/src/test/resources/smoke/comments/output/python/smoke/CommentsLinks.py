

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Comments import Comments

class CommentsLinks(_NativeBase):
    """The nested types like [random_method] don't need full name prefix, but it's
possible to references other interfaces like [smoke.CommentsInterface] or other members
[comments.someMethodWithAllComments].

Weblinks are not modified like this [example1], [example2](http://www.example.com/2) or https://www.example.com/3.

[example1]: http://example.com/1"""
    def __init__(self, native):
        super().__init__(native)

    def random_method(*args, **kwargs) -> Comments.SomeEnum:
        """Link types:
* constant: [comments.VeryUseful]
* struct: [comments.SomeStruct]
* struct field: [comments.SomeStruct.someField]
* enum: [comments.SomeEnum]
* enum item: [comments.SomeEnum.USEFUL]
* property: [comments.SomeProperty]
* property setter: [comments.SomeProperty.set]
* property getter: [comments.SomeProperty.get]
* method: [comments.someMethodWithAllComments]
* method with signature: [comments.oneParameterCommentOnly(String, String)]
* method with signature with no spaces: [comments.oneParameterCommentOnly(String,String)]
* parameter: [inputParameter]
* top level constant: [CommentsTypeCollection.TypeCollectionConstant]
* top level struct: [CommentsTypeCollection.TypeCollectionStruct]
* top level struct field: [CommentsTypeCollection.TypeCollectionStruct.field]
* top level enum: [CommentsTypeCollection.TypeCollectionEnum]
* top level enum item: [CommentsTypeCollection.TypeCollectionEnum.item]
* error: [comments.SomethingWrong]
* lambda: [comments.SomeLambda]
* type from aux sources, same package: [AuxClass]
* type from aux sources, different package: [fire.AuxStruct]
  * we can also have
  * nested lists

Not working for Java:
* typedef: [comments.Usefulness]
* top level typedef: [CommentsTypeCollection.TypeCollectionTypedef]

Not working for Swift:
* named comment: [Alternative name for the link, stripped for Swift][comments.VeryUseful]"""
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
            """Some random field [comments.SomeStruct]"""
            return _wrap(self._native.random_field, Comments.SomeStruct)
        @random_field.setter
        def random_field(self, value: Comments.SomeStruct):
          self._native.random_field = _unwrap(value, Comments.SomeStruct)
    
    
    

