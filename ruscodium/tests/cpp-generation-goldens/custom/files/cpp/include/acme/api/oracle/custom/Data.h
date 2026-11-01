// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "acme/api/oracle/custom/RenamedService.h"
#include "acme/detail/ExportAcmeApi.h"
#include "acme/detail/VectorHash.h"
#include <memory>
#include <string>
#include <vector>

namespace acme {
namespace api {

namespace oracle {



namespace custom {

    class Worker;


}


}
}
}

namespace acme {
namespace api {
namespace oracle {
namespace custom {
struct ACME_API_EXPORT Data {
    ::std::vector< ::std::string > values;
    ::acme::api::oracle::custom::RenamedService::Nested nested;
    ::std::shared_ptr< ::acme::api::oracle::custom::Worker > worker = ::std::shared_ptr< ::acme::api::oracle::custom::Worker >();

    Data( );
    Data( ::std::vector< ::std::string > values, ::acme::api::oracle::custom::RenamedService::Nested nested );
    Data( ::std::vector< ::std::string > values, ::acme::api::oracle::custom::RenamedService::Nested nested, ::std::shared_ptr< ::acme::api::oracle::custom::Worker > worker );

};


}
}
}
}
