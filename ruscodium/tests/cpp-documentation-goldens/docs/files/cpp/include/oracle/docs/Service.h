// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include "TypeRepository.h"
#include <cstdint>

namespace oracle {
namespace docs {
/**
 * A café description with C++ text in order.
 *
 * A second paragraph with configured replacement.

 */
class _GLUECODIUM_CPP_EXPORT Service {
public:
    Service();
    virtual ~Service();


public:
    /**
     * Transforms input.
     * \param[in] value Input value.
     * \return Result value.
     */
    virtual int32_t transform( const int32_t value ) = 0;
    /**
     *
     * \private
     */
    virtual void hidden(  ) = 0;
    /**
     * Reads the value.
     * \return Current value.
     */
    virtual int32_t get_value(  ) const = 0;
    /**
     * Writes the value.
     * \param[in] value Current value.
     */
    virtual void set_value( const int32_t value ) = 0;

};


}
}
