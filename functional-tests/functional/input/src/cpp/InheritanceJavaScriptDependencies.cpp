#include "test/ConstructorOverloads.h"

#include <memory>

namespace test
{
namespace
{
class ConstructorOverloadsImpl: public ConstructorOverloads
{
public:
    ~ConstructorOverloadsImpl( ) override = default;
};

}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( const std::string& )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( const bool )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( const std::string&, const bool )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( const std::vector< double >& )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

std::shared_ptr< ConstructorOverloads >
ConstructorOverloads::create( const uint64_t )
{
    return std::make_shared< ConstructorOverloadsImpl >( );
}

}