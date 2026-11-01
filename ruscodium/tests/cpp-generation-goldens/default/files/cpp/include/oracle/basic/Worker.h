// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include "TypeRepository.h"
#include <cstdint>
#include <string>

namespace oracle {
namespace basic {
class _GLUECODIUM_CPP_EXPORT Worker {
public:
    Worker();
    virtual ~Worker();


public:
    virtual ::std::string run( const int32_t value ) = 0;
    virtual bool is_ready(  ) const = 0;
    virtual void set_ready( const bool value ) = 0;

    virtual ::std::string get_name(  ) const = 0;

    static int32_t get_version(  );

};


}
}
