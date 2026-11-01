#include "smoke/LambdaComments.h"
#include <cassert>
#include <string>
int main() {
    smoke::LambdaComments::WithNamedParameters fn = [](const std::string& text) { return text + "!"; };
    assert(fn("hi") == "hi!");
}
