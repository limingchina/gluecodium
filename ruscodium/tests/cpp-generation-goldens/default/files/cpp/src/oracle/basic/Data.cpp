// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#include "oracle/basic/Data.h"
#include <utility>

namespace oracle {
namespace basic {

Data::Data( )
    : label{ }, mapping{ }
{
}


Data::Data( ::std::string label )
    : label( std::move( label ) )
{
}


}
}

