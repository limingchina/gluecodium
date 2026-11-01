// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#include "acme/api/oracle/custom/RenamedService.h"
#include "acme/api/oracle/custom/Worker.h"
#include <utility>

namespace acme {
namespace api {
namespace oracle {
namespace custom {
RenamedService::RenamedService() {
}
RenamedService::~RenamedService() {
}


RenamedService::Nested::Nested( )
    : amount{ }
{
}

RenamedService::Nested::Nested( int32_t amount )
    : amount( std::move( amount ) )
{
}


}
}
}
}

