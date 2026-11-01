// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#include "smoke/CommentsInterface.h"
#include <utility>

namespace smoke {
CommentsInterface::CommentsInterface() {
}
CommentsInterface::~CommentsInterface() {
}




CommentsInterface::SomeStruct::SomeStruct( )
    : some_field{ }
{
}

CommentsInterface::SomeStruct::SomeStruct( ::smoke::CommentsInterface::Usefulness some_field )
    : some_field( std::move( some_field ) )
{
}

const ::smoke::CommentsInterface::Usefulness CommentsInterface::VERY_USEFUL = true;

}

