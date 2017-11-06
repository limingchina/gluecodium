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

#include "hello/SimpleInstantiable.h"
#include "hello/NestedInstantiable.h"

namespace hello
{
class HelloWorldSimpleInstantiable : public SimpleInstantiable
{
public:
    virtual void set_string_value( const ::std::string& string_value ) override;
    virtual ::std::string get_string_value( ) override;

private:
    ::std::string m_string_value = "";
};

class HelloWorldNestedInstantiable : public NestedInstantiable
{
public:
    HelloWorldNestedInstantiable(
        const ::std::shared_ptr< ::hello::SimpleInstantiable >& instance );

    virtual void set_instantiable(
        const ::std::shared_ptr< ::hello::SimpleInstantiable >& instance ) override;
    virtual ::std::shared_ptr< ::hello::SimpleInstantiable > get_instantiable( ) override;

private:
    ::std::shared_ptr< ::hello::SimpleInstantiable > m_instance = nullptr;
};
}
