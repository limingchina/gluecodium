// -------------------------------------------------------------------------------------------------
//
//
// -------------------------------------------------------------------------------------------------
#pragma once
#include "genium/Export.h"
#include <string>
namespace smoke {
class _GENIUM_CPP_EXPORT SimpleClass {
public:
    SimpleClass();
    virtual ~SimpleClass() = 0;
public:
virtual ::std::string get_string_value(  ) = 0;
};
}