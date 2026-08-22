#include <emscripten/bind.h>
#include <vector>
#include <map>
#include <string>
using namespace emscripten;

std::vector<int> makeVec() { return {1,2,3}; }
std::map<std::string, int> makeMap() { return {{"a",1},{"b",2}}; }

EMSCRIPTEN_BINDINGS(spike5) {
    register_vector<int>("VectorInt");
    register_map<std::string, int>("MapStringInt");
    function("makeVec", &makeVec);
    function("makeMap", &makeMap);
}
