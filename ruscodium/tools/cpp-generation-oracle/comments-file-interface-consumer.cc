#include "smoke/CommentsInterface.h"
#include <cassert>
int main() {
    smoke::CommentsInterface::SomeStruct value(true);
    assert(value.some_field);
    assert(smoke::CommentsInterface::VERY_USEFUL);
}
