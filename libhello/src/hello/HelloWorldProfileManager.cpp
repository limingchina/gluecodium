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

#include <string>
#include <memory>
#include "hello/HelloWorldStaticLogger.h"
#include "HelloWorldProfileManager.h"

namespace hello
{

// ProfileManager destruction is logged to static logger to allow verification of correct instance disposal
HelloWorldProfileManager::~HelloWorldProfileManager( )
{
    HelloWorldStaticLogger::append( "ProfileManager::destructor" );
}

void
HelloWorldProfileManager::create_profile( const ::std::string& username )
{
    m_profile_name = username;
}

::std::string
HelloWorldProfileManager::change_profile( const ::std::string& username )
{
    std::string old = m_profile_name;
    m_profile_name = username;
    return old;
}

::std::string
HelloWorldProfileManager::delete_profile( )
{
    std::string old = m_profile_name;
    m_profile_name = "";
    return old;
}
}
