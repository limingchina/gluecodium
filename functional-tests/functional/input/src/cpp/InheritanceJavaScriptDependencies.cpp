#include "test/ConstructorOverloads.h"
#include "test/ThrowingConstructor.h"

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

class ThrowingConstructorImpl: public ThrowingConstructor
{
public:
    ~ThrowingConstructorImpl( ) override = default;
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

lorem_ipsum::test::Return< std::shared_ptr< ThrowingConstructor >, std::error_code >
ThrowingConstructor::create( const double input )
{
    return input == 0 ? lorem_ipsum::test::Return< std::shared_ptr< ThrowingConstructor >,
                                                   std::error_code >(
                            std::make_shared< ThrowingConstructorImpl >( ) )
                      : std::error_code( ThrowingConstructor::ErrorEnum::CRASHED );
}
}