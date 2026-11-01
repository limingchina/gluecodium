// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#include "oracle/docs/Data.h"
#include <utility>

namespace oracle {
namespace docs {

Data::Data( )
    : label{ }, count{ }
{
}


Data::Data( ::std::string label, int32_t count )
    : label( std::move( label ) ), count( std::move( count ) )
{
}


}
}

