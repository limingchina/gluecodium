// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include "Optional.h"
#include "UnorderedMapHash.h"
#include <cstdint>
#include <string>
#include <unordered_map>

namespace oracle {
namespace basic {
struct _GLUECODIUM_CPP_EXPORT Data {
    int32_t count = 7;
    ::std::string label;
    ::optional< int32_t > maybe = ::optional< int32_t >();
    ::std::unordered_map< ::std::string, int32_t > mapping;

    Data( );

    explicit Data( ::std::string label );


};


}
}
