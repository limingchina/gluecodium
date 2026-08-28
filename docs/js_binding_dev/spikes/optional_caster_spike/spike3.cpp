#include <emscripten/bind.h>
#include <optional>
using namespace emscripten;

std::optional<int> getOpt(bool present) { return present ? std::optional<int>(42) : std::nullopt; }
void takeOpt(std::optional<int> v) { printf("takeOpt has=%d\n", (int)v.has_value()); }

EMSCRIPTEN_BINDINGS(spike3) {
    register_optional<int>();
    function("getOpt", &getOpt);
    function("takeOpt", &takeOpt);
}
