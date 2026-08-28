#include "test/SomeOpenNumberWrapperClass.h"

#include <memory>

namespace test
{
class SomeOpenNumberWrapperClassImpl : public SomeOpenNumberWrapperClass {
public:
    explicit SomeOpenNumberWrapperClassImpl( int n )
        : m_number{ n }
    {}

    ~SomeOpenNumberWrapperClassImpl() override = default;

    int32_t get_number() const override {
        return m_number;
    }

    void set_number( const int32_t value ) override {
        m_number = value;
    }

private:
    int m_number{};
};

std::shared_ptr<SomeOpenNumberWrapperClass>
SomeOpenNumberWrapperClass::make( const int32_t n ) {
    return std::make_shared<SomeOpenNumberWrapperClassImpl>( n );
}
}  // namespace test
