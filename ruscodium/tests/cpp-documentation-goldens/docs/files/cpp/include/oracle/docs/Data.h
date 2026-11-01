// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"
#include <cstdint>
#include <string>

namespace oracle {
namespace docs {
/**
 * A data container.

 */
struct _GLUECODIUM_CPP_EXPORT Data {
    /**
     * Label text.

     */
    ::std::string label;
    /**
     * Count text.

     */
    int32_t count;

    /**
     * Constructs data.
     */
    Data( );
    /**
     * Constructs data.


     * \param label Label text.


     * \param count Count text.

     */

    Data( ::std::string label, int32_t count );


};


}
}
