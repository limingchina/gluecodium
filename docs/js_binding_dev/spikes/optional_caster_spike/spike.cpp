#include <emscripten/bind.h>
#include <optional>
#include <string>
using namespace emscripten;

// Attempt 1: does embind support std::optional<T> natively?
struct Foo { int x = 0; std::string s; };

std::optional<int> getOpt(bool present) { return present ? std::optional<int>(42) : std::nullopt; }
std::optional<Foo> getOptFoo() { return Foo{7, "hi"}; }

EMSCRIPTEN_BINDINGS(spike) {
    value_object<Foo>("Foo")
        .field("x", &Foo::x)
        .field("s", &Foo::s);
    function("getOpt", &getOpt);
    function("getOptFoo", &getOptFoo);
}
