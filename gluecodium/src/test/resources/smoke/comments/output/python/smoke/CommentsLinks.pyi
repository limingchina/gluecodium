

from smoke.commentsSomeEnum import commentsSomeEnum
from smoke.commentsSomeStruct import commentsSomeStruct

from _native_base import _NativeBase

import generated


class CommentsLinks(_NativeBase):
    """The nested types like [random_method] don't need full name prefix, but it's
possible to references other interfaces like [smoke.CommentsInterface] or other members
[comments.someMethodWithAllComments].

Weblinks are not modified like this [example1], [example2](http://www.example.com/2) or https://www.example.com/3.

[example1]: http://example.com/1"""

    def __init__(self, native):
        super().__init__(native)

    def random_method(self, input_parameter: commentsSomeEnum) -> commentsSomeEnum:
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
        return self._native.random_method(input_parameter._native)

    def random_method(self, text: str, flag: bool):
        """Links to method overloads:
* other one: [random_method(SomeEnum)]
* this one: [random_method(String, Boolean)]
* ambiguous one: [random_method]"""
        return self._native.random_method(text, flag)

