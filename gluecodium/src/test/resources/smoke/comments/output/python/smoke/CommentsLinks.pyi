

from smoke.Comments import Comments
from enum import Enum
import typing

class CommentsLinks:
    """The nested types like `CommentsLinks.random_method` don't need full name prefix, but it's
possible to references other interfaces like `CommentsInterface` or other members
`Comments.some_method_with_all_comments`.

Weblinks are not modified like this [example1], [example2](http://www.example.com/2) or https://www.example.com/3.

[example1]: http://example.com/1"""

    def random_method(self, input_parameter: Comments.SomeEnum) -> Comments.SomeEnum:
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
        ...

    def random_method(self, text: str, flag: bool):
        """Links to method overloads:
* other one: `CommentsLinks.random_method`
* this one: `CommentsLinks.random_method`
* ambiguous one: `CommentsLinks.random_method`"""
        ...

    class RandomStruct:
        """Links also work in:"""
    
        #: Some random field `Comments.SomeStruct`
        random_field: Comments.SomeStruct
    
    

