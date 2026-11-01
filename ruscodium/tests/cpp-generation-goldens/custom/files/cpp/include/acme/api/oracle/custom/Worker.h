// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "acme/detail/ExportAcmeApi.h"
#include "acme/detail/TypeRepository.h"
#include <cstdint>

namespace acme {
namespace api {
namespace oracle {
namespace custom {
class ACME_API_EXPORT Worker {
public:
    Worker();
    virtual ~Worker();


public:
    virtual int32_t process( const int32_t value ) = 0;
};


}
}
}
}
