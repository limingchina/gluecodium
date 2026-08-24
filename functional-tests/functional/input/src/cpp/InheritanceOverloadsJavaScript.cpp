#include "test/ChildClassFromClassOverloads.h"
#include "test/InheritanceOverloadsTestHelper.h"

#include <memory>

namespace test
{
namespace
{
class ChildClassFromClassOverloadsImpl: public ChildClassFromClassOverloads
{
public:
    void foo( ) override { }
    void foo( const int32_t ) override { }
    void bar( ) override { }
    void baz( ) override { }
    void foo( const std::string& ) override { }
    void bar( const std::string& ) override { }
};
}

std::shared_ptr< ChildClassFromClassOverloads >
InheritanceOverloadsTestHelper::create_class_overloads( )
{
    return std::make_shared< ChildClassFromClassOverloadsImpl >( );
}
}  // namespace test