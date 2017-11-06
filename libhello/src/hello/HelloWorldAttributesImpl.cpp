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

#include "HelloWorldAttributesImpl.h"

namespace hello
{

HelloWorldAttributesImpl::~HelloWorldAttributesImpl( ) = default;

uint32_t
HelloWorldAttributesImpl::get_built_in_type_attribute( )
{
    return m_build_in_type_attribute;
}

void
HelloWorldAttributesImpl::set_built_in_type_attribute( const uint32_t value )
{
    m_build_in_type_attribute = value;
}

float
HelloWorldAttributesImpl::get_readonly_attribute( )
{
    return m_read_only_attribute;
}

::hello::HelloWorldAttributes::ExampleStruct
HelloWorldAttributesImpl::get_struct_attribute( )
{
    return m_struct_attribute;
}

void
HelloWorldAttributesImpl::set_struct_attribute(
    const ::hello::HelloWorldAttributes::ExampleStruct& value )
{
    m_struct_attribute = value;
}

}
