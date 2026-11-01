// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include "oracle/basic/Shade.h"
#include <functional>
#include <string>

namespace oracle {
namespace basic {
using Callback = ::std::function<::std::string(const ::oracle::basic::Shade)>;


}
}
