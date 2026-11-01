// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#include "acme/api/oracle/custom/Data.h"
#include "acme/api/oracle/custom/Worker.h"
#include <utility>

namespace acme {
namespace api {
namespace oracle {
namespace custom {

Data::Data( )
    : values{ }, nested{ }
{
}

Data::Data( ::std::vector< ::std::string > values, ::acme::api::oracle::custom::RenamedService::Nested nested )
    : values( std::move( values ) ), nested( std::move( nested ) )
{
}
Data::Data( ::std::vector< ::std::string > values, ::acme::api::oracle::custom::RenamedService::Nested nested, ::std::shared_ptr< ::acme::api::oracle::custom::Worker > worker )
    : values( std::move( values ) ), nested( std::move( nested ) ), worker( std::move( worker ) )
{
}


}
}
}
}

