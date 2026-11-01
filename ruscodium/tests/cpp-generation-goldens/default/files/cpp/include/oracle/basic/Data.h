// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include "Optional.h"
#include "UnorderedMapHash.h"
#include "UnorderedSetHash.h"
#include <cstdint>
#include <string>
#include <unordered_map>
#include <unordered_set>

namespace oracle {
namespace basic {
struct _GLUECODIUM_CPP_EXPORT Data {
    using EarlierAlias = int32_t;

    using LaterAlias = ::oracle::basic::Data::EarlierAlias;

    int32_t count = 7;
    ::std::string label;
    ::optional< int32_t > maybe = ::optional< int32_t >();
    ::std::unordered_map< ::std::string, int32_t > mapping;
    ::std::unordered_set< ::std::string > tags;

    Data( );

    explicit Data( ::std::string label );


};


}
}
