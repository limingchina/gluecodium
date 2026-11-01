// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "acme/detail/ExportAcmeApi.h"
#include <cstdint>
#include <memory>
#include <string>

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
class ACME_API_EXPORT RenamedService {
public:
    RenamedService();
    virtual ~RenamedService();


public:
    struct ACME_API_EXPORT Nested {
        int32_t amount;

        Nested( );
        explicit Nested( int32_t amount );

    };

    using InnerAlias = ::acme::api::oracle::custom::RenamedService::Nested;

public:
    /**
     *
     * \param[in] worker @NotNull
     * \param[in] count
     * \return
     */
    virtual ::std::string use( const ::std::shared_ptr< ::acme::api::oracle::custom::Worker >& worker, const int32_t count ) = 0;
    virtual int32_t get_value(  ) const = 0;
    virtual void set_value( const int32_t value ) = 0;

};


}
}
}
}
