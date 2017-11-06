// -------------------------------------------------------------------------------------------------
//
// Copyright (C) 2017 HERE Global B.V. and/or its affiliated companies. All rights reserved.
//
// This software, including documentation, is protected by copyright controlled by
// HERE Global B.V. All rights are reserved. Copying, including reproducing, storing,
// adapting or translating, any or all of this material requires the prior written
// consent of HERE Global B.V. This material also contains confidential information,
// which may not be disclosed to others without prior written consent of HERE Global B.V.
//
// -------------------------------------------------------------------------------------------------

#include "test/TypeCollection.h"
#include "test/StaticTypedef.h"

namespace test
{

StaticTypedef::IntTypedef
StaticTypedef::return_int_typedef( const ::test::StaticTypedef::IntTypedef input )
{
    return input + 1;
}

StaticTypedef::NestedIntTypedef
StaticTypedef::return_nested_int_typedef( const ::test::StaticTypedef::NestedIntTypedef input )
{
    return input + 1;
}

StaticTypedef::StringTypedef
StaticTypedef::return_string_typedef( const ::test::StaticTypedef::StringTypedef& input )
{
    return "Hello " + input;
}

StaticTypedef::ByteArrayTypedef
StaticTypedef::return_byte_buffer_typedef( const ::test::StaticTypedef::ByteArrayTypedef& input )
{
    return { input.rbegin(), input.rend() };
}

StaticTypedef::ExampleStructTypedef
StaticTypedef::return_example_struct_typedef( const ::test::StaticTypedef::ExampleStructTypedef& input )
{
    StaticTypedef::ExampleStructTypedef result;
    result.example_string = "Hello " + input.example_string;
    return result;
}

::test::PointTypedef
StaticTypedef::return_typedef_point_from_type_collection( const ::test::PointTypedef& input )
{
    return input;
}

StaticTypedef::NestedStructTypedef
StaticTypedef::return_nested_struct_typedef( const ::test::StaticTypedef::NestedStructTypedef& input )
{
    StaticTypedef::NestedStructTypedef result;
    result.example_string = "Hello " + input.example_string;
    return result;
}

}
