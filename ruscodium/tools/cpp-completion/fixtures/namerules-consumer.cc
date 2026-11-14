#include <namerules/customNameRules.h>
#include <cassert>
#include <cstdint>
#include <vector>
int main() {
    auto object = namerules::customNameRules::create();
    assert(object);
    object->STORE_INT_ATTRIBUTE_NOW(42);
    object->STORE_BOOLEAN_ATTRIBUTE_NOW(true);
    assert(object->retrieve_int_attribute() == 42);
    assert(object->really_boolean_attribute());
    namerules::customNameRules::exampleStruct value(1.25, std::vector<int64_t>{2, 3});
    object->STORE_STRUCT_ATTRIBUTE_NOW(value);
    assert(object->retrieve_struct_attribute().m_double_value == 1.25);
    assert(object->retrieve_struct_attribute().m_int_values.size() == 2);
    auto result = object->someMethod(value);
    assert(!result.has_value());
    assert(result.error() == namerules::customNameRules::exampleErrorCode::FATAL_ENTRY);
}
