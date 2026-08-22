#include <emscripten/bind.h>

#include "phase4/Harness.h"

namespace phase4 {

int32_t Harness::add(const int32_t first, const int32_t second) {
    return first + second;
}

}  // namespace phase4
