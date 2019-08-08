// -------------------------------------------------------------------------------------------------
//
//
// -------------------------------------------------------------------------------------------------
//
// Automatically generated. Do not modify. Your changes will be lost.
//
// -------------------------------------------------------------------------------------------------
#pragma once
#include "genium/Export.h"
#include "genium/Return.h"
#include "smoke/Comments.h"
#include <system_error>
namespace smoke {
/**
 * The nested types like ::smoke::CommentsLinks::random_method don't need full name prefix, but it's
 * possible to references other interfaces like ::smoke::CommentsInterface or other members
 * ::smoke::Comments::some_method_with_all_comments.
 *
 * Weblinks are not modified like this [example] or [www.example.com].
 *
 * [example]: http://example.com
 */
class _GENIUM_CPP_EXPORT CommentsLinks {
public:
    virtual ~CommentsLinks() = 0;
public:
/**
 * Link types:
 * * constant: ::smoke::Comments::VERY_USEFUL
 * * struct: ::smoke::Comments::SomeStruct
 * * struct field: ::smoke::Comments::SomeStruct::some_field
 * * enum: ::smoke::Comments::SomeEnum
 * * enum item: ::smoke::Comments::SomeEnum::USEFUL
 * * attribute: ::smoke::Comments::is_some_attribute
 * * attribute setter: ::smoke::Comments::set_some_attribute
 * * attribute getter: ::smoke::Comments::is_some_attribute
 * * method: ::smoke::Comments::instance_method
 * * top level constant: ::smoke::TYPE_COLLECTION_CONSTANT
 * * top level struct: ::smoke::TypeCollectionStruct
 * * top level struct field: ::smoke::TypeCollectionStruct::field
 * * top level enum: ::smoke::TypeCollectionEnum
 * * top level enum item: ::smoke::TypeCollectionEnum::ITEM
 * * error: ::smoke::Comments::SomeEnum
 *
 * Not working for Java:
 * * typedef: ::smoke::Comments::Usefulness
 * * array: ::smoke::Comments::SomeArray
 * * map: ::smoke::Comments::SomeMap
 * * top level typedef: ::smoke::TypeCollectionTypedef
 *
 * Not working for Swift:
 * * named comment: [Alternative name for the link, stripped for Swift]::smoke::Comments::VERY_USEFUL
 *
 * Not working:
 * * input parameter: input_parameter
 * * output parameter: [outputParameter]
 * \param[in] input_parameter Sometimes takes ::smoke::Comments::SomeEnum::USEFUL
 * \return Sometimes returns ::smoke::Comments::SomeEnum::USEFUL
 * \retval ::smoke::Comments::SomeEnum May or may not throw ::smoke::Comments::SomeEnum
 */
virtual ::genium::Return< ::smoke::Comments::SomeEnum, ::std::error_code > random_method( const ::smoke::Comments::SomeEnum input_parameter ) = 0;
};
}
