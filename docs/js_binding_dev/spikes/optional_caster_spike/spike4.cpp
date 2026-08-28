#include <emscripten/bind.h>
#include <optional>
#include <string>
#include <map>
#include <vector>
using namespace emscripten;

// Return<T,E> from Gluecodium's Return.h — emulate with a struct here
struct Ret { std::optional<int> value; std::optional<std::string> error; };
Ret divide(int a, int b) {
    if (b == 0) return {std::nullopt, std::string("division by zero")};
    return {a / b, std::nullopt};
}

EMSCRIPTEN_BINDINGS(spike4) {
    register_optional<int>();
    register_optional<std::string>();
    value_object<Ret>("Ret")
        .field("value", &Ret::value)
        .field("error", &Ret::error);
    function("divide", &divide);
}
