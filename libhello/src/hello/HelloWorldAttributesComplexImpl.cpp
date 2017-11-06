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

#include "HelloWorldAttributesComplexImpl.h"

namespace hello
{

HelloWorldAttributesComplexImpl::~HelloWorldAttributesComplexImpl( ) = default;

::std::vector< ::std::string >
HelloWorldAttributesComplexImpl::get_array_attribute( )
{
    return m_array_attribute;
}

void
HelloWorldAttributesComplexImpl::set_array_attribute( const ::std::vector< ::std::string >& value )
{
    m_array_attribute = value;
}

::hello::HelloWorldAttributesComplex::InternalError
HelloWorldAttributesComplexImpl::get_complex_type_attribute( )
{
    return m_complex_type_attribute;
}

void
HelloWorldAttributesComplexImpl::set_complex_type_attribute(
    const ::hello::HelloWorldAttributesComplex::InternalError value )
{
    m_complex_type_attribute = value;
}

}
